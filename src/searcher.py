import time
import random
from gui import show_sale_type_dialog, show_property_type_dialog, show_location_input_dialog, show_location_options_dialog, show_price_range_dialog, show_space_input_dialog, show_loading_message, log_message, show_failure_screen, close_gui
import asyncio
class NavigationState:
    def __init__(self):
        self.step_stack = []
        self.data = {}
        
    def push_step(self, step_name, data=None):
        self.step_stack.append(step_name)
        if data:
            self.data[step_name] = data
            
    def pop_step(self):
        if len(self.step_stack) > 0:
            removed_step = self.step_stack.pop()
            # Clear data for all steps that come after the current step
            self.clear_subsequent_data()
            return removed_step
        return None
        
    def clear_subsequent_data(self):
        """Clear data for steps that come after current step in navigation"""
        step_order = ['sale_type', 'property_type', 'location_input', 'location_options', 'price_range', 'space_input']
        current_step = self.get_current_step()
        
        if current_step:
            try:
                current_index = step_order.index(current_step)
                # Clear data for all subsequent steps
                for step in step_order[current_index + 1:]:
                    if step in self.data:
                        del self.data[step]
            except ValueError:
                pass  # Current step not in order list
        
    def get_current_step(self):
        return self.step_stack[-1] if self.step_stack else None
        
    def get_previous_step(self):
        return self.step_stack[-2] if len(self.step_stack) > 1 else None

async def select_autocomplete_option(context):
    page = await context.new_page()
    nav_state = NavigationState()
    max_retries = 3

    for attempt in range(max_retries):
        try:
            show_loading_message(f"Connecting to LoopNet.ca (Attempt {attempt + 1}/{max_retries})...")
            log_message(f"🔄 Attempt {attempt + 1} to access LoopNet.ca")

            await page.goto("https://www.loopnet.ca/", wait_until="domcontentloaded", timeout=30000)
            page_content = await page.content()

            if "access denied" in page_content.lower() or "blocked" in page_content.lower() or "403" in page_content:
                log_message(f"⚠️ Access denied detected on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    log_message("🔄 Refreshing page and retrying...")
                    await asyncio.sleep(random.uniform(2, 4))
                    continue
                else:
                    log_message("❌ Access denied after all retry attempts")
                    show_failure_screen()
                    return None

            log_message("✅ Successfully connected to LoopNet.ca")
            await asyncio.sleep(random.uniform(0.5, 1))
            await page.reload(wait_until="domcontentloaded")
            await asyncio.sleep(random.uniform(0.5, 1))
            break

        except Exception as e:
            log_message(f"⚠️ Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                log_message("🔄 Retrying in a few seconds...")
                await asyncio.sleep(random.uniform(3, 6))
            else:
                log_message("❌ Failed to connect after all attempts")
                show_failure_screen()
                return None

    
    # Main navigation flow
    current_step = 'sale_type'
    
    while current_step:
        if current_step == 'sale_type':
            result = handle_sale_type_step(page, nav_state)
            if result == 'cancelled':
                return None
            elif result == 'back':
                current_step = None  # Exit - first step
            else:
                current_step = 'property_type'
                
        elif current_step == 'property_type':
            result = handle_property_type_step(page, nav_state)
            if result == 'cancelled':
                return None
            elif result == 'back':
                current_step = 'sale_type'
                # Need to re-execute browser actions for sale type
                continue
            else:
                current_step = 'location_input'
                
        elif current_step == 'location_input':
            result = handle_location_input_step(page, nav_state)
            if result == 'cancelled':
                return None
            elif result == 'back':
                current_step = 'property_type'
                continue
            else:
                current_step = 'location_options'
                
        elif current_step == 'location_options':
            result = handle_location_options_step(page, nav_state)
            if result == 'cancelled':
                return None
            elif result == 'back':
                current_step = 'location_input'
                continue
            else:
                current_step = 'price_range'
                
        elif current_step == 'price_range':
            result = handle_price_range_step(page, nav_state)
            if result == 'cancelled':
                return None
            elif result == 'back':
                current_step = 'location_options'
                continue
            elif result == 'skip':
                current_step = 'space_input'
            else:
                current_step = 'space_input'
                
        elif current_step == 'space_input':
            result = handle_space_input_step(page, nav_state)
            if result == 'cancelled':
                return None
            elif result == 'back':
                current_step = 'price_range'
                continue
            else:
                current_step = None  # Complete
    
    final_url = page.url
    log_message(f"🌐 Redirected to: {final_url}")
    
    show_loading_message("Setup complete! Preparing search results...")
    time.sleep(2)
    
    page.close()
    log_message("🔄 Search setup complete, ready for data collection")
    
    return final_url

def handle_sale_type_step(page, nav_state):
    sale_type_options = {
        0: {"label": "For Lease", "selector": "li.long-name:has-text('For Lease')"},
        1: {"label": "For Sale", "selector": "li.long-name[ng-click=\"selectSearchType('forSale')\"]"},
    }
    
    try:
        page.wait_for_selector("li.long-name", timeout=10000)
    except:
        log_message("⚠️ Page elements may not be fully loaded")
    
    nav_state.push_step('sale_type')
    result = show_sale_type_dialog(sale_type_options)
    
    if result is None:
        return 'cancelled'
    elif isinstance(result, dict) and result.get('action') == 'back':
        return 'back'
    
    # Execute the selection
    locator = page.locator(sale_type_options[result]["selector"])
    locator.wait_for(state="visible", timeout=5000)
    locator.click()
    log_message(f"✅ Selected: {sale_type_options[result]['label']}")
    
    nav_state.data['sale_type_choice'] = result
    time.sleep(random.uniform(0.5, 1))
    return 'continue'

def handle_property_type_step(page, nav_state):
    page.wait_for_selector("div.property-type-icons div.property-type", timeout=10000)
    
    prop_types_section = page.locator("div.property-type-icons")
    prop_type_tiles = prop_types_section.locator("div.property-type")
    
    prop_count = prop_type_tiles.count()
    prop_options = {}
    
    for i in range(prop_count):
        tile = prop_type_tiles.nth(i)
        try:
            label = tile.locator("p.bold").inner_text().strip()
            if not label:
                label = tile.inner_text().strip()
            prop_options[i] = {"text": label, "element": tile}
        except Exception as e:
            log_message(f"⚠️ Error reading property type {i}: {e}")
    
    log_message("🏢 Property Types retrieved")
    
    nav_state.push_step('property_type')
    result = show_property_type_dialog(prop_options)
    
    if result is None:
        return 'cancelled'
    elif isinstance(result, dict) and result.get('action') == 'back':
        nav_state.pop_step()
        return 'back'
    
    # Execute the selection
    prop_options[result]["element"].click()
    log_message(f"✅ Selected Property Type: {prop_options[result]['text']}")
    
    nav_state.data['selected_prop'] = result
    nav_state.data['prop_options'] = prop_options
    time.sleep(random.uniform(0.5, 1))
    return 'continue'

def handle_location_input_step(page, nav_state):
    nav_state.push_step('location_input')
    result = show_location_input_dialog()
    
    if result is None:
        return 'cancelled'
    elif isinstance(result, dict) and result.get('action') == 'back':
        nav_state.pop_step()
        return 'back'
    
    nav_state.data['keyword'] = result
    log_message(f"🔎Using location keyword: {result}")
    return 'continue'

def handle_location_options_step(page, nav_state):
    keyword = nav_state.data['keyword']
    
    show_loading_message("Waiting for location suggestions...")
    
    # Clear the input field first and then type the new keyword
    location_input = page.locator("input[name='geography']:visible")
    location_input.click()
    location_input.fill('')  # Clear existing content
    time.sleep(0.5)  # Small delay to ensure clearing
    location_input.type(keyword, delay=100)
    
    popup = page.locator("ul.typeahead-popup")
    try:
        popup.wait_for(state="visible", timeout=10000)
    except:
        log_message("❌ Autocomplete popup did not appear.")
        return 'cancelled'
    
    options = {}
    li_elements = popup.locator("li[role='option']")
    count = li_elements.count()
    
    for i in range(count):
        li = li_elements.nth(i)
        a = li.locator("a")
        try:
            text = a.inner_text().strip()
            options[i] = {"text": text, "element": li}
        except Exception as e:
            log_message(f"⚠️ Error reading item {i}: {e}")
    
    log_message("📍 Location Suggestions retrieved")
    
    nav_state.push_step('location_options')
    result = show_location_options_dialog(options)
    
    if result is None:
        return 'cancelled'
    elif isinstance(result, dict) and result.get('action') == 'back':
        nav_state.pop_step()
        return 'back'
    
    # Execute the selection
    previous_url = page.url
    options[result]["element"].click()
    log_message(f"✅ Selected: {options[result]['text']}")
    
    # Wait for URL to change
    try:
        page.wait_for_url(lambda url: url != previous_url, timeout=10000)
    except Exception:
        log_message("⚠️ URL did not change after location selection, waiting for load event instead.")
        page.wait_for_load_state("load")
    
    nav_state.data['selected_location'] = result
    nav_state.data['location_options'] = options
    time.sleep(random.uniform(0.5, 1))
    return 'continue'

def handle_price_range_step(page, nav_state):
    sale_type_choice = nav_state.data['sale_type_choice']
    
    # Setup price form based on sale type
    if sale_type_choice == 0:  # For Lease
        dropdown_selector = "div.search-bar-for-lease-filters div.drop-down.lease-rate.custom"
        form_name = "frmSearchBarLeaseRate"
    else:  # For Sale
        dropdown_selector = "div.search-bar-for-sale-filters div.drop-down.sale-price.custom"
        form_name = "frmSearchBarPriceRange"
    
    show_loading_message("Fetching price range filter options...")
    
    dropdown_button = page.locator(dropdown_selector)
    try:
        dropdown_button.wait_for(state="visible", timeout=10000)
        dropdown_button.click()
    except Exception as e:
        log_message(f"⚠️ Could not click dropdown button: {e}")
        return 'cancelled'
    
    price_form = page.locator(f'form[name="{form_name}"]')
    try:
        price_form.wait_for(state="visible", timeout=10000)
        
        pills = price_form.locator('div.pill:not(.ng-hide)')
        pill_count = pills.count()
        
        log_message(f"🪙 Found {pill_count} price range options")
        pill_options = {}
        
        for i in range(pill_count):
            pill = pills.nth(i)
            try:
                label_element = pill.locator('label')
                label_text = label_element.inner_text().strip()
                pill_options[i] = {"text": label_text, "element": label_element}
            except Exception as e:
                log_message(f"⚠️ Error reading pill {i}: {e}")
        
        nav_state.push_step('price_range')
        result = show_price_range_dialog(pill_options)
        
        if result is None:
            return 'cancelled'
        elif isinstance(result, dict) and result.get('action') == 'back':
            nav_state.pop_step()
            return 'back'
        elif result == "skip":
            log_message("⏭️ Skipping price range selection...")
            nav_state.data['selected_price'] = 'skip'
            return 'skip'
        
        # Handle combined result from new GUI
        if isinstance(result, dict) and 'price_type' in result:
            price_type_idx = result['price_type']
            min_value = result['min_value']
            max_value = result['max_value']
            
            # Step 1: Execute the price type selection first
            log_message(f"🎯 Selecting price range type: {pill_options[price_type_idx]['text']}")
            pill_options[price_type_idx]["element"].click()
            log_message(f"✅ Clicked price range type: {pill_options[price_type_idx]['text']}")
            
            # Small delay to let the form update
            time.sleep(random.uniform(0.5, 1))
            
            # Step 2: Enter min/max values if provided
            if min_value or max_value:
                log_message(f"💰 Entering price values - Min: {min_value or 'None'}, Max: {max_value or 'None'}")
                
                try:
                    # Find the price input fields after clicking the price type
                    text_inputs = price_form.locator('input[type="text"]')
                    input_count = text_inputs.count()
                    
                    if input_count >= 2:
                        # Enter minimum value
                        if min_value:
                            min_input = text_inputs.first
                            min_input.clear()
                            min_input.type(min_value)
                            log_message(f"✅ Entered minimum price: {min_value}")
                            
                        # Enter maximum value  
                        if max_value:
                            max_input = text_inputs.nth(1)
                            max_input.clear()
                            max_input.type(max_value)
                            log_message(f"✅ Entered maximum price: {max_value}")
                            
                        show_loading_message("Applying price filter...")
                        
                        # Wait for page to redirect after entering values
                        previous_url = page.url
                        try:
                            page.wait_for_url(lambda url: url != previous_url, timeout=10000)
                            log_message("✅ Page redirected after price filter application")
                        except Exception:
                            log_message("⚠️ URL did not change after filter, waiting for load event instead.")
                            page.wait_for_load_state("load")
                        
                        time.sleep(random.uniform(0.5, 1))
                        
                    else:
                        log_message(f"⚠️ Expected 2 text inputs, found {input_count}")
                        
                except Exception as e:
                    log_message(f"⚠️ Error entering price values: {e}")
            else:
                log_message("ℹ️ No price values provided, proceeding with price type selection only")
            
            # Store the data
            nav_state.data['selected_price'] = price_type_idx
            nav_state.data['pill_options'] = pill_options
            nav_state.data['price_values'] = {'min': min_value, 'max': max_value}
            return 'continue'
        else:
            # Handle simple price type selection (fallback)
            log_message(f"🎯 Simple price type selection: {pill_options[result]['text']}")
            pill_options[result]["element"].click()
            log_message(f"✅ Selected price range type: {pill_options[result]['text']}")
            
            nav_state.data['selected_price'] = result
            nav_state.data['pill_options'] = pill_options
            return 'continue'
        
    except Exception as e:
        log_message(f"⚠️ Error with price range form: {e}")
        return 'cancelled'


def handle_space_input_step(page, nav_state):
    sale_type_choice = nav_state.data['sale_type_choice']
    
    # Setup space form based on sale type
    if sale_type_choice == 0:  # For Lease
        space_dropdown_selector = "div.search-bar-for-lease-filters div.drop-down.space-available.custom"
        space_form_name = "frmSearchBarSpaceAvailable"
    else:  # For Sale
        space_dropdown_selector = "div.search-bar-for-sale-filters div.drop-down.building-size.custom"
        space_form_name = "frmSearchBarBuildingSize"
    
    space_dropdown = page.locator(space_dropdown_selector)
    try:
        space_dropdown.wait_for(state="visible", timeout=10000)
        space_dropdown.click()
        
        nav_state.push_step('space_input')
        result = show_space_input_dialog()
        
        if result is None:
            return 'cancelled'
        elif isinstance(result, dict) and result.get('action') == 'back':
            nav_state.pop_step()
            return 'back'
        elif result == "skip":
            log_message("⏭️ Skipping space filter...")
            return 'continue'
        
        # Execute the input
        min_space = result['min']
        max_space = result['max']
        
        space_form = page.locator(f'form[name="{space_form_name}"]')
        try:
            space_form.wait_for(state="attached", timeout=5000)
            
            sf_inputs = space_form.locator('input[type="text"][placeholder*="SF"]')
            sf_count = sf_inputs.count()
            
            if min_space and sf_count > 0:
                min_input = sf_inputs.first
                min_input.fill(min_space, force=True)
                
            if max_space and sf_count > 1:
                max_input = sf_inputs.nth(1)
                max_input.fill(max_space, force=True)
            elif max_space and sf_count == 1:
                log_message("⚠️ Only found one SF input, cannot set maximum")
            
            if min_space or max_space:
                show_loading_message("Applying space filter...")
                previous_url = page.url
                try:
                    page.wait_for_url(lambda url: url != previous_url, timeout=10000)
                except Exception:
                    log_message("⚠️ URL did not change after space filter selection, waiting for load event instead.")
                    page.wait_for_load_state("load")
                
                time.sleep(random.uniform(0.5, 1))
                
        except Exception as e:
            log_message(f"⚠️ Error with space form: {e}")
            
        nav_state.data['space_input'] = result
        return 'continue'
        
    except Exception as e:
        log_message(f"⚠️ Could not click space available dropdown: {e}")
        return 'cancelled'