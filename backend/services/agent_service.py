import asyncio
import json
import os
from playwright.async_api import async_playwright, Page
from services.gemini_service import GeminiService
import base64

class AutoApplyAgent:
    def __init__(self, headless=False):
        self.headless = headless
        self.gemini = GeminiService()
        self.status_log = []
        
    def log(self, message):
        """Add a message to the status log"""
        print(f"[Agent] {message}")
        self.status_log.append(message)
    
    async def analyze_page(self, page: Page):
        """Use Gemini Vision to analyze the page and identify form fields"""
        self.log("Analyzing page structure...")
        
        # Take a screenshot
        screenshot_bytes = await page.screenshot()
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
        
        # Get page HTML for context
        html_snippet = await page.content()
        # Truncate HTML to avoid token limits
        html_snippet = html_snippet[:5000] if len(html_snippet) > 5000 else html_snippet
        
        prompt = f"""You are an autonomous job application agent. Analyze this job application page.
        
Page HTML (truncated):
{html_snippet}

Return a JSON object with the following structure:
{{
    "apply_button_selector": "CSS selector for the Apply button (or null if not found)",
    "form_fields": [
        {{
            "label": "Field label or purpose (e.g., 'First Name', 'Email')",
            "selector": "CSS selector for the input field",
            "type": "text|email|tel|file|select|radio|checkbox"
        }}
    ],
    "captcha_detected": true/false,
    "page_type": "job_listing|application_form|thank_you"
}}

Be precise with CSS selectors. Look for common patterns like input[name="firstName"], input[type="email"], etc.
"""
        
        try:
            # Note: Gemini Vision API would need the screenshot
            # For now, we'll use text-only analysis
            response = self.gemini.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            analysis = json.loads(response.text)
            self.log(f"Page analysis complete: {analysis.get('page_type', 'unknown')}")
            return analysis
        except Exception as e:
            self.log(f"Error analyzing page: {e}")
            return {
                "apply_button_selector": None,
                "form_fields": [],
                "captcha_detected": False,
                "page_type": "unknown"
            }
    
    async def fill_form_field(self, page: Page, field_info, user_profile):
        """Fill a single form field based on its label/type"""
        try:
            selector = field_info['selector']
            label = field_info['label'].lower()
            field_type = field_info['type']
            
            # Determine what value to fill based on label
            value = None
            if 'first' in label and 'name' in label:
                value = user_profile.get('full_name', '').split()[0] if user_profile.get('full_name') else None
            elif 'last' in label and 'name' in label:
                parts = user_profile.get('full_name', '').split()
                value = parts[-1] if len(parts) > 1 else None
            elif 'email' in label:
                value = user_profile.get('email')
            elif 'phone' in label:
                value = user_profile.get('phone')
            elif 'linkedin' in label:
                value = user_profile.get('linkedin_url')
            elif 'github' in label:
                value = user_profile.get('github_url')
            elif 'portfolio' in label or 'website' in label:
                value = user_profile.get('portfolio_url')
            
            if value and field_type in ['text', 'email', 'tel']:
                await page.fill(selector, value)
                self.log(f"Filled {label}: {value[:20]}...")
                return True
            
            return False
        except Exception as e:
            self.log(f"Error filling field {field_info.get('label')}: {e}")
            return False
    
    async def upload_resume(self, page: Page, resume_path):
        """Upload resume file"""
        try:
            # Look for file input
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(resume_path)
                self.log(f"Uploaded resume: {os.path.basename(resume_path)}")
                return True
            else:
                self.log("No file upload field found")
                return False
        except Exception as e:
            self.log(f"Error uploading resume: {e}")
            return False
    
    async def start_application(self, job_url, user_profile, resume_path):
        """Main entry point for the agent"""
        self.log(f"Starting application for: {job_url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Navigate to job page
                self.log("Navigating to job page...")
                await page.goto(job_url, wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(2000)  # Wait for dynamic content
                
                # Analyze the page
                analysis = await self.analyze_page(page)
                
                # Check for CAPTCHA
                if analysis.get('captcha_detected'):
                    self.log("CAPTCHA detected! Manual intervention required.")
                    if not self.headless:
                        self.log("Browser is visible. Please solve the CAPTCHA and press Enter in terminal...")
                        # In a real implementation, we'd wait for user input
                        await page.wait_for_timeout(30000)
                    else:
                        return {
                            'success': False,
                            'status': 'captcha_detected',
                            'log': self.status_log
                        }
                
                # If it's a job listing page, click Apply button
                if analysis.get('page_type') == 'job_listing' and analysis.get('apply_button_selector'):
                    self.log("Clicking Apply button...")
                    await page.click(analysis['apply_button_selector'])
                    await page.wait_for_timeout(2000)
                    
                    # Re-analyze after clicking
                    analysis = await self.analyze_page(page)
                
                # Fill form fields
                if analysis.get('form_fields'):
                    self.log(f"Found {len(analysis['form_fields'])} form fields")
                    for field in analysis['form_fields']:
                        if field['type'] == 'file':
                            await self.upload_resume(page, resume_path)
                        else:
                            await self.fill_form_field(page, field, user_profile)
                
                # Take a screenshot before submitting
                screenshot_path = os.path.join('output', f'pre_submit_{os.path.basename(resume_path)}.png')
                await page.screenshot(path=screenshot_path)
                self.log(f"Screenshot saved: {screenshot_path}")
                
                # Look for submit button
                submit_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Submit")',
                    'button:has-text("Apply")'
                ]
                
                submitted = False
                for selector in submit_selectors:
                    try:
                        submit_btn = await page.query_selector(selector)
                        if submit_btn:
                            self.log(f"Found submit button: {selector}")
                            # In production, you might want to pause here for confirmation
                            # await submit_btn.click()
                            # submitted = True
                            self.log("Submit button found but NOT clicked (safety measure)")
                            break
                    except:
                        continue
                
                # Check if we're on a thank you page
                current_url = page.url
                if 'thank' in current_url.lower() or 'success' in current_url.lower():
                    self.log("Application submitted successfully!")
                    return {
                        'success': True,
                        'status': 'applied',
                        'log': self.status_log
                    }
                
                return {
                    'success': True,
                    'status': 'form_filled',
                    'log': self.status_log,
                    'screenshot': screenshot_path
                }
                
            except Exception as e:
                self.log(f"Error during application: {str(e)}")
                return {
                    'success': False,
                    'status': 'error',
                    'error': str(e),
                    'log': self.status_log
                }
            finally:
                await browser.close()
