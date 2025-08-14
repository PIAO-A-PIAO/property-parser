import time
import random
from gui import show_sale_type_dialog, show_property_type_dialog, show_location_input_dialog, show_location_options_dialog, show_price_range_dialog, show_price_input_dialog, show_space_input_dialog, show_loading_message, log_message, show_failure_screen, close_gui

def select_autocomplete_option(context):
        page = context.new_page()
        
        # Retry logic for accessing loopnet.ca
        max_retries = 3
        for attempt in range(max_retries):
            try:
                show_loading_message(f"Connecting to LoopNet.ca (Attempt {attempt + 1}/{max_retries})...")
                log_message(f"🔄 Attempt {attempt + 1} to access LoopNet.ca")
                
                page.goto("https://www.loopnet.ca/", wait_until="domcontentloaded", timeout=30000)
                
                # Check for access denied or blocked content
                page_content = page.content()
                if "access denied" in page_content.lower() or "blocked" in page_content.lower() or "403" in page_content:
                    log_message(f"⚠️ Access denied detected on attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        log_message("🔄 Refreshing page and retrying...")
                        # Simulate manual refresh with F5
                        time.sleep(random.uniform(2, 4))
                        page.evaluate("window.location.reload(true)")
                        page.wait_for_load_state("domcontentloaded")
                        time.sleep(random.uniform(1, 2))
                        continue
                    else:
                        # Final attempt failed
                        log_message("❌ Access denied after all retry attempts")
                        show_failure_screen()
                        return None
                
                # Success - page loaded properly
                log_message("✅ Successfully connected to LoopNet.ca")
                
                # Simulate manual refresh for good measure
                time.sleep(random.uniform(0.5, 1))
                page.evaluate("window.location.reload(true)")
                page.wait_for_load_state("domcontentloaded")        
                time.sleep(random.uniform(0.5, 1))
                break
                
            except Exception as e:
                log_message(f"⚠️ Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    log_message(f"🔄 Retrying in a few seconds...")
                    time.sleep(random.uniform(3, 6))
                else:
                    log_message("❌ Failed to connect after all attempts")
                    show_failure_screen()
                    return None

        #####################
        ### 1. SALE TYPE ###
        #####################

        sale_type_options = {
            0: {"label": "For Lease", "selector": "li.long-name:has-text('For Lease')"},
            1: {"label": "For Sale", "selector": "li.long-name[ng-click=\"selectSearchType('forSale')\"]"},
            # 2: {"label": "Businesses For Sale", "selector": "li.long-name:has-text('Businesses For Sale')"}
        }

        try:
            page.wait_for_selector("li.long-name", timeout=10000)
        except:
            log_message("⚠️ Page elements may not be fully loaded")

        # Show GUI dialog for sale type selection
        sale_type_choice = show_sale_type_dialog(sale_type_options)
        
        if sale_type_choice is None:
            log_message("❌ Selection cancelled by user")
            context.close()
            return None
            
        # Wait for sale type option to be visible and click it
        locator = page.locator(sale_type_options[sale_type_choice]["selector"])
        locator.wait_for(state="visible", timeout=5000)
        locator.click()
        log_message(f"✅ Selected: {sale_type_options[sale_type_choice]['label']}")

        time.sleep(random.uniform(0.5, 1))

        ###########################
        ### 2. PROPERTY TYPE ###
        ###########################

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

        # Show GUI dialog for property type selection
        selected_prop = show_property_type_dialog(prop_options)
        
        if selected_prop is None:
            log_message("❌ Property type selection cancelled by user")
            context.close()
            return None
            
        prop_options[selected_prop]["element"].click()
        log_message(f"✅ Selected Property Type: {prop_options[selected_prop]['text']}")

        time.sleep(random.uniform(0.5, 1))

        #############################
        ### 3. LOCATION AUTOCOMPLETE ###
        #############################
        
        # Show GUI dialog for location input
        keyword = show_location_input_dialog()
        
        if keyword is None:
            log_message("❌ Location input cancelled by user")
            context.close()
            return None
            
        log_message(f"🔎Using location keyword: {keyword}")
        show_loading_message(f"Waiting for location suggestions...")

        location_input = page.locator("input[name='geography']:visible")
        location_input.click()
        location_input.type(keyword, delay=100)

        popup = page.locator("ul.typeahead-popup")
        try:
            popup.wait_for(state="visible", timeout=10000)
        except:
            log_message("❌ Autocomplete popup did not appear.")
            context.close()
            return None

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

        # Show GUI dialog for location options selection
        selected_location = show_location_options_dialog(options)
        
        if selected_location is None:
            log_message("❌ Location selection cancelled by user")
            context.close()
            return None
            
        previous_url = page.url
        options[selected_location]["element"].click()
        log_message(f"✅ Selected: {options[selected_location]['text']}")

        # Wait for URL to change after selection (up to 10 seconds)
        try:
            page.wait_for_url(lambda url: url != previous_url, timeout=10000)
        except Exception:
            log_message("⚠️ URL did not change after location selection, waiting for load event instead.")
            page.wait_for_load_state("load")

        # Extra delay for dynamic content to settle
        time.sleep(random.uniform(0.5, 1))

        #############################
        ### 4. PRICE FILTER ###
        #############################
        
        # Click the appropriate dropdown button based on sale type choice
        if sale_type_choice == 0:  # For Lease
            dropdown_selector = "div.search-bar-for-lease-filters div.drop-down.lease-rate.custom"
            form_name = "frmSearchBarLeaseRate"
        else:  # For Sale
            dropdown_selector = "div.search-bar-for-sale-filters div.drop-down.sale-price.custom"
            form_name = "frmSearchBarPriceRange"
        show_loading_message(f"Fetching price range filter options...")

        # Click the dropdown button to make the form visible
        dropdown_button = page.locator(dropdown_selector)
        try:
            dropdown_button.wait_for(state="visible", timeout=10000)
            dropdown_button.click()
        except Exception as e:
            log_message(f"⚠️ Could not click dropdown button: {e}")
            
        price_form = page.locator(f'form[name="{form_name}"]')
        try:
            price_form.wait_for(state="visible", timeout=10000)
            
            # Get all pills that are not hidden
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
                    pass
                except Exception as e:
                    log_message(f"⚠️ Error reading pill {i}: {e}")
            
            # Show GUI dialog for price range selection
            selected_price = show_price_range_dialog(pill_options)
            
            if selected_price is None:
                log_message("❌ Price range selection cancelled by user")
                context.close()
                return None
            elif selected_price == "skip":
                log_message("⏭️ Skipping price range selection...")
                # Skip directly to step 5 (space filter)
            else:
                pill_options[selected_price]["element"].click()
                log_message(f"✅ Selected price range type: {pill_options[selected_price]['text']}")
                
                # Show price input GUI with the selected unit
                unit_label = pill_options[selected_price]['text']
                unit_with_currency = f"CAD/{unit_label}"
                price_input = show_price_input_dialog(unit_with_currency)
                
                if price_input is None:
                    log_message("❌ Price input cancelled by user")
                    context.close()
                    return None
                elif price_input == "skip":
                    log_message("⏭️ Skipping price value entry...")
                else:
                    min_value = price_input['min']
                    max_value = price_input['max']
                    
                    # Find and fill the text inputs
                    try:
                        if min_value:
                            min_input = price_form.locator('input[type="text"]').first
                            min_input.clear()
                            min_input.type(min_value)
                            
                        if max_value:
                            max_input = price_form.locator('input[type="text"]').nth(1)
                            max_input.clear()
                            max_input.type(max_value)
                            
                        if min_value or max_value:
                            show_loading_message("Applying price filter...")
                    except Exception as e:
                        log_message(f"⚠️ Error entering values: {e}")
                    
                    # Wait for page to redirect after entering values
                    previous_url = page.url
                    try:
                        page.wait_for_url(lambda url: url != previous_url, timeout=10000)
                        log_message("✅ Page redirected after price filter selection")
                    except Exception:
                        log_message("⚠️ URL did not change after filter selection, waiting for load event instead.")
                        page.wait_for_load_state("load")
                    
                    time.sleep(random.uniform(0.5, 1))  # Extra delay for dynamic content to settle
            
        except Exception as e:
            log_message(f"⚠️ Error with price range form: {e}")

        #############################
        ### 5. SPACE AVAILABLE FILTER ###
        #############################
        
        # Click the appropriate space dropdown based on sale type choice
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

            # Show space input GUI
            space_input = show_space_input_dialog()
            
            if space_input is None:
                log_message("❌ Space input cancelled by user")
                context.close()
                return None
            elif space_input == "skip":
                log_message("⏭️ Skipping space filter...")
            else:
                min_space = space_input['min']
                max_space = space_input['max']
                
                space_form = page.locator(f'form[name="{space_form_name}"]')
                try:
                    space_form.wait_for(state="attached", timeout=5000)
                    
                    # Find text inputs with "SF" in placeholder
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
                        
                    # Wait for page to redirect after entering space values
                    if min_space or max_space:
                        show_loading_message("Applying space filter...")
                        previous_url = page.url
                        try:
                            page.wait_for_url(lambda url: url != previous_url, timeout=10000)
                        except Exception:
                            log_message("⚠️ URL did not change after space filter selection, waiting for load event instead.")
                            page.wait_for_load_state("load")
                        
                        time.sleep(random.uniform(0.5, 1))  # Extra delay for dynamic content to settle
                
                except Exception as e:
                    log_message(f"⚠️ Error with space form: {e}")
                
        except Exception as e:
            log_message(f"⚠️ Could not click space available dropdown: {e}")

        final_url = page.url
        log_message(f"🌐 Redirected to: {final_url}")

        # Show final loading message
        show_loading_message("Setup complete! Preparing search results...")
        time.sleep(2)  # Give user time to see the final message

        page.close()
        
        # Keep GUI open for web parsing phase - don't close yet
        log_message("🔄 Search setup complete, ready for data collection")
        
        return final_url
