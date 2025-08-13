import time
import random

def select_autocomplete_option(context):
        page = context.new_page()
        page.goto("https://www.loopnet.ca/", wait_until="domcontentloaded")
        
        # Simulate manual refresh with F5
        time.sleep(random.uniform(0.5, 1))
        page.evaluate("window.location.reload(true)")
        page.wait_for_load_state("load")        
        time.sleep(random.uniform(1.0, 2.0))

        #####################
        ### 1. SALE TYPE ###
        #####################

        sale_type_options = {
            0: {"label": "For Lease", "selector": "li.long-name:has-text('For Lease')"},
            1: {"label": "For Sale", "selector": "li.long-name[ng-click=\"selectSearchType('forSale')\"]"},
            # 2: {"label": "Businesses For Sale", "selector": "li.long-name:has-text('Businesses For Sale')"}
        }

        # Wait for the sale type options to be fully loaded before showing UI
        try:
            page.wait_for_selector("li.long-name", timeout=10000)
        except:
            print("⚠️ Page elements may not be fully loaded")

        print("\n📌 What are you looking for?")
        for idx, val in sale_type_options.items():
            print(f"{idx}: {val['label']}")

        while True:
            try:
                sale_type_choice = int(input("👉 Select by number: "))
                if sale_type_choice in sale_type_options:
                    # Wait for sale type option to be visible and click it
                    locator = page.locator(sale_type_options[sale_type_choice]["selector"])
                    locator.wait_for(state="visible", timeout=5000)
                    locator.click()
                    print(f"✅ Selected: {sale_type_options[sale_type_choice]['label']}")
                    break
                else:
                    print("❌ Invalid number. Try again.")
            except ValueError:
                print("❌ Please enter a number.")

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
                print(f"⚠️ Error reading property type {i}: {e}")

        print("\n🏢 Property Types:")
        for idx, val in prop_options.items():
            print(f"{idx}: {val['text']}")

        while True:
            try:
                selected_prop = int(input("👉 Select property type by number: "))
                if selected_prop in prop_options:
                    prop_options[selected_prop]["element"].click()
                    print(f"✅ Selected Property Type: {prop_options[selected_prop]['text']}")
                    break
                else:
                    print("❌ Invalid number. Try again.")
            except ValueError:
                print("❌ Please enter a number.")

        time.sleep(random.uniform(0.5, 1))

        #############################
        ### 3. LOCATION AUTOCOMPLETE ###
        #############################
        keyword = input("\n🗺️ Enter a location keyword (e.g., Toronto, Warehouse, etc.): ")
        location_input = page.locator("input[name='geography']:visible")
        location_input.click()
        location_input.type(keyword, delay=100)

        popup = page.locator("ul.typeahead-popup")
        try:
            popup.wait_for(state="visible", timeout=10000)
        except:
            print("❌ Autocomplete popup did not appear.")
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
                print(f"⚠️ Error reading item {i}: {e}")

        print("📍 Location Suggestions:")
        for idx, val in options.items():
            print(f"{idx}: {val['text']}")

        while True:
            try:
                selection = int(input("👉 Which location do you mean? Enter number: "))
                if selection in options:
                    previous_url = page.url
                    options[selection]["element"].click()
                    print(f"✅ Selected: {options[selection]['text']}")
                    break
                else:
                    print("❌ Invalid number. Try again.")
            except ValueError:
                print("❌ Please enter a number.")

        # Wait for URL to change after selection (up to 10 seconds)
        try:
            page.wait_for_url(lambda url: url != previous_url, timeout=10000)
        except Exception:
            print("⚠️ URL did not change after location selection, waiting for load event instead.")
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
            
        # Click the dropdown button to make the form visible
        dropdown_button = page.locator(dropdown_selector)
        try:
            dropdown_button.wait_for(state="visible", timeout=10000)
            dropdown_button.click()
        except Exception as e:
            print(f"⚠️ Could not click dropdown button: {e}")
            
        price_form = page.locator(f'form[name="{form_name}"]')
        try:
            price_form.wait_for(state="visible", timeout=10000)
            
            # Get all pills that are not hidden
            pills = price_form.locator('div.pill:not(.ng-hide)')
            pill_count = pills.count()
            
            print(f"\n🪙 Found {pill_count} price range options:")
            pill_options = {}
            
            for i in range(pill_count):
                pill = pills.nth(i)
                try:
                    label_element = pill.locator('label')
                    label_text = label_element.inner_text().strip()
                    pill_options[i] = {"text": label_text, "element": label_element}
                    print(f"{i}: {label_text}")
                except Exception as e:
                    print(f"⚠️ Error reading pill {i}: {e}")
            
            # Ask user to choose a price range option
            while True:
                try:
                    user_input = input("👉 Select price range type by number (or press Enter to skip): ")
                    if user_input.strip() == "":
                        print("⏭️ Skipping price range selection...")
                        break
                    choice = int(user_input)
                    if choice in pill_options:
                        pill_options[choice]["element"].click()
                        print(f"✅ Selected price range type: {pill_options[choice]['text']}")
                        
                        # Ask for min and max values
                        min_value = input("👉 Enter minimum value (or press Enter to skip): ").strip()
                        max_value = input("👉 Enter maximum value (or press Enter to skip): ").strip()
                        
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
                        except Exception as e:
                            print(f"⚠️ Error entering values: {e}")
                        
                        # Wait for page to redirect after entering values
                        previous_url = page.url
                        try:
                            page.wait_for_url(lambda url: url != previous_url, timeout=10000)
                            print("✅ Page redirected after price filter selection")
                        except Exception:
                            print("⚠️ URL did not change after filter selection, waiting for load event instead.")
                            page.wait_for_load_state("load")
                        
                        time.sleep(random.uniform(0.5, 1))  # Extra delay for dynamic content to settle
                        
                        break
                    else:
                        print("❌ Invalid number. Try again.")
                except ValueError:
                    print("❌ Please enter a number.")
            
        except Exception as e:
            print(f"⚠️ Error with price range form: {e}")

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

            print("\n🏢 Filter by size: ")                
            # Ask for min and max space values
            min_space = input("👉 Enter minimum space (or press Enter to skip): ").strip()
            max_space = input("👉 Enter maximum space (or press Enter to skip): ").strip()
            
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
                    print("⚠️ Only found one SF input, cannot set maximum")
                    
                # Wait for page to redirect after entering space values
                if min_space or max_space:
                    previous_url = page.url
                    try:
                        page.wait_for_url(lambda url: url != previous_url, timeout=10000)
                    except Exception:
                        print("⚠️ URL did not change after space filter selection, waiting for load event instead.")
                        page.wait_for_load_state("load")
                    
                    time.sleep(random.uniform(0.5, 1))  # Extra delay for dynamic content to settle
                
            except Exception as e:
                print(f"⚠️ Error with space form: {e}")
                
        except Exception as e:
            print(f"⚠️ Could not click space available dropdown: {e}")

        final_url = page.url
        print(f"\n🌐 Redirected to: {final_url}")

        page.close()
        return final_url
