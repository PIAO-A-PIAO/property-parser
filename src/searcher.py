import time

def select_autocomplete_option(context):
        page = context.new_page()
        page.goto("https://www.loopnet.ca/", wait_until="domcontentloaded")

        #####################
        ### 1. SALE TYPE ###
        #####################

        sale_type_options = {
            0: {"label": "For Lease", "selector": "li.long-name:has-text('For Lease')"},
            1: {"label": "For Sale", "selector": "li.long-name:has-text('For Sale')"},
            2: {"label": "Businesses For Sale", "selector": "li.long-name:has-text('Businesses For Sale')"}
        }

        print("\n📌 What are you looking for?")
        for idx, val in sale_type_options.items():
            print(f"{idx}: {val['label']}")

        while True:
            try:
                choice = int(input("👉 Select by number: "))
                if choice in sale_type_options:
                    # Wait for sale type option to be visible and click it
                    locator = page.locator(sale_type_options[choice]["selector"])
                    locator.wait_for(state="visible", timeout=5000)
                    locator.click()
                    print(f"✅ Selected: {sale_type_options[choice]['label']}")
                    break
                else:
                    print("❌ Invalid number. Try again.")
            except ValueError:
                print("❌ Please enter a number.")

        time.sleep(1)

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

        time.sleep(1)

        #############################
        ### 3. LOCATION AUTOCOMPLETE ###
        #############################
        keyword = input("Enter a location keyword (e.g., Toronto, Warehouse, etc.): ")
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

        print("\n📍 Location Suggestions:")
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
        time.sleep(2)

        final_url = page.url
        print(f"🌐 Redirected to: {final_url}")

        page.close()
        return final_url
