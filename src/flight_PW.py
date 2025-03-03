from playwright.sync_api import sync_playwright

def run(playwright, where_from, where_to, departure_date, return_date, max_time):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the URL
    page.goto("https://www.google.com/travel/flights")
    page.wait_for_load_state("domcontentloaded")
    
    # Enter "Columbus" in the "Where from?" field
    page.get_by_role("combobox", name="Where from?").fill(where_from)
    page.get_by_text(where_from).click()
    
    # Enter "St. Maarten" in the "Where to?" field
    page.get_by_role("combobox", name="Where to?").fill(where_to)
    page.get_by_text(where_to).click()

    # Enter "07/12/2025" in the "Departure" field
    page.get_by_placeholder("Departure").first.click()
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="Departure").click()
    page.get_by_role("textbox", name="Departure").fill(departure_date)

    # Enter "07/19/2025" in the "Return" field
    page.get_by_role("textbox", name="Return").click()
    page.get_by_role("textbox", name="Return").fill(return_date)
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(1000)

    # Click the "Search" button
    page.get_by_role("button", name="Search").click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    # Click the "View more flights" button            
    try:
        page.get_by_role("button", name="View more flights").click(timeout=800)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)
    except:
        pass
    
    # Find the cheapest round trip cost for the 1-stop and Nonstop flights
    non_stop_flight_costs = page.locator("//div[@role='tabpanel'][1]//span[text()='Nonstop']/../../following-sibling::div//span[contains(text(), '$')]").all()
    one_stop_flight_costs = page.locator("//div[@role='tabpanel'][1]//span[text()='1 stop']/../../following-sibling::div//span[contains(text(), '$')]").all()

    # Get the details for the cheapest round trip flight that is under the max time
    def get_cheapest_round_trip_cost(flight_costs):
        cheapest_amount = 999999
        cheapest_departure_element = []
        cheapest_return_element = []
        cheapest_departure_duration = ""
        cheapest_return_duration = ""
        cheapest_departure_flight_time = ""
        cheapest_departure_arrival_time = ""
        cheapest_return_flight_time = ""
        cheapest_return_arrival_time = ""
        cheapest_departure_airline = ""
        cheapest_return_airline = ""

        for dep_flight in flight_costs:
            # Get the travel time
            departure_duration = dep_flight.locator("//../../../..//div[contains(@aria-label,'Total duration')]").inner_text()
            travel_hrs = departure_duration.split(" ")[0]
            #print("Departing travel time: ", departure_duration)

            # Check if the travel time is less than the max time
            if int(travel_hrs) < max_time:

                # Get the cost amount
                cost_amount = int(dep_flight.inner_text().replace("$", "").replace(",", ""))

                # Get the departure and arrival times
                departure_flight_time = dep_flight.locator("//../../../..//span[contains(@aria-label,'Departure time')]/span").inner_text()
                departure_arrival_time = dep_flight.locator("//../../../..//span[contains(@aria-label,'Arrival time')]/span").inner_text()
                #print(f"Departure flight time: {departure_flight_time}, Departure arrival time: {departure_arrival_time}")

                # Get the airline name
                departure_airline_name = dep_flight.locator("//../../../../div[1]/following-sibling::div[1]/div[2]/span[1]").inner_text()
                #print(f"Departing Airline: {departure_airline_name}")

                # Click on the element to select the return flight
                dep_flight.click()
                page.wait_for_load_state("domcontentloaded")

                # Click the "View more flights" button
                viewed_more_flights = True
                try:
                    page.get_by_role("button", name="View more flights").click(timeout=500)
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(1000)
                except:
                    viewed_more_flights = False
                    pass

                # Get the costs for the return flights
                return_flights = page.locator("//div[contains(@aria-label,'Total duration')]/../../div/following-sibling::div//*[contains(text(), '$')]").all()

                for return_flight in return_flights:
                    # Get the travel time
                    return_duration = return_flight.locator("//../../../..//div[contains(@aria-label,'Total duration')]").inner_text()
                    travel_hrs = return_duration.split(" ")[0]
                    #print("Returning travel time: ", return_duration)

                    # Check if the travel time is less than the max time
                    if int(travel_hrs) < max_time:

                        # Get the cost amount
                        cost_amount = int(return_flight.inner_text().replace("$", "").replace(",", ""))

                        # Check if the cost amount is less than the cheapest amount
                        if cost_amount < cheapest_amount:

                            # Get the return flight times
                            return_flight_time = return_flight.locator("//../../../..//span[contains(@aria-label,'Departure time')]/span[@role='text']").inner_text()
                            return_home_time = return_flight.locator("//../../../..//span[contains(@aria-label,'Arrival time')]/span[@role='text']").inner_text()
                            #print(f"Return flight time: {departure_flight_time}, Return home time: {departure_arrival_time}")
                            
                            # Get the airline name
                            return_airline_name = return_flight.locator("//../../../../div[1]/following-sibling::div[1]/div[2]/span[1]").inner_text()
                            #print(f"Departing Airline: {return_airline_name}")

                            # Update the cheapest element, amount, travel time, departure time, and arrival time
                            cheapest_amount = cost_amount

                            cheapest_departure_element = dep_flight
                            cheapest_departure_airline = departure_airline_name
                            cheapest_departure_duration = departure_duration
                            cheapest_departure_flight_time = departure_flight_time
                            cheapest_departure_arrival_time = departure_arrival_time

                            cheapest_return_element = return_flight
                            cheapest_return_airline = return_airline_name
                            cheapest_return_duration = return_duration
                            cheapest_return_flight_time = return_flight_time
                            cheapest_return_arrival_time = return_home_time

                # Click the browser back button to go back to the search results
                page.go_back()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(1000)
                if viewed_more_flights:
                    page.go_back()
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(1000)

        return cheapest_amount, cheapest_departure_element, cheapest_departure_airline, cheapest_departure_duration, cheapest_departure_flight_time, cheapest_departure_arrival_time, cheapest_return_element, cheapest_return_airline, cheapest_return_duration, cheapest_return_flight_time, cheapest_return_arrival_time


    cheapest_nonstop_amount = 999999
    cheapest_one_stop_amount = 999999
    # Print the cheapest Nonstop flight
    if len(non_stop_flight_costs) > 0:
        cheapest_nonstop_amount, cheapest_non_stop_departure_element, cheapest_non_stop_departure_airline, cheapest_non_stop_dep_duration, cheapest_non_stop_departure_time, cheapest_non_stop_arrival_time, cheapest_non_stop_return_element, cheapest_non_stop_return_airline, cheapest_non_stop_return_duration, cheapest_non_stop_return_flight_time, cheapest_non_stop_return_arrival_time = get_cheapest_round_trip_cost(non_stop_flight_costs)
        print(f"Cheapest Nonstop round trip flight under {max_time} hours: ${cheapest_nonstop_amount}")

        print(f"Departing Airline: {cheapest_non_stop_departure_airline}")
        print(f"Departure Travel Duration: {cheapest_non_stop_dep_duration}")
        print(f"Departure Flight Time: {cheapest_non_stop_departure_time}")
        print(f"Destination Arrival Time: {cheapest_non_stop_arrival_time}\n")

        print(f"Returning Airline: {cheapest_non_stop_return_airline}")
        print(f"Return Travel Duration: {cheapest_non_stop_return_duration}")
        print(f"Return Flight Time: {cheapest_non_stop_return_flight_time}")
        print(f"Return Home Time: {cheapest_non_stop_return_arrival_time}")


    # Print the cheapest 1-stop flight
    if len(one_stop_flight_costs) > 0:
        cheapest_one_stop_amount, cheapest_one_stop_departure_element, cheapest_one_departure_airline, cheapest_one_stop_departure_duration, cheapest_one_stop_departure_time, cheapest_one_stop_arrival_time, cheapest_one_stop_return_element, cheapest_one_stop_return_airline, cheapest_one_stop_return_duration, cheapest_one_stop_return_flight_time, cheapest_one_stop_return_arrival_time = get_cheapest_round_trip_cost(one_stop_flight_costs)
        print(f"Cheapest 1-stop round trip flight under {max_time} hours: ${cheapest_one_stop_amount}")
        print(f"Departing Airline: {cheapest_one_departure_airline}")
        print(f"Departure Travel Duration: {cheapest_one_stop_departure_duration}")
        print(f"Departure Flight Time: {cheapest_one_stop_departure_time}")
        print(f"Destination Arrival Time: {cheapest_one_stop_arrival_time}\n")

        print(f"Returning Airline: {cheapest_one_stop_return_airline}")
        print(f"Return Travel Duration: {cheapest_one_stop_return_duration}")
        print(f"Return Flight Time: {cheapest_one_stop_return_flight_time}")
        print(f"Return Home Time: {cheapest_one_stop_return_arrival_time}")


    # Compare the cheapest Nonstop and 1-stop flight
    if cheapest_nonstop_amount < cheapest_one_stop_amount:
        print("The cheapest flight is the Nonstop flight")
        cheapest_non_stop_departure_element.click()
        page.wait_for_load_state("domcontentloaded")
        cheapest_non_stop_return_element.click()
        page.wait_for_load_state("domcontentloaded")
        # Get the url of the page
        url = page.url
        print(url)
        
        # Close the browser
        browser.close()
        return url, cheapest_nonstop_amount, cheapest_non_stop_departure_airline, cheapest_non_stop_dep_duration, cheapest_non_stop_departure_time, cheapest_non_stop_arrival_time, cheapest_non_stop_return_element, cheapest_non_stop_return_airline, cheapest_non_stop_return_duration, cheapest_non_stop_return_flight_time, cheapest_non_stop_return_arrival_time
    else:
        print("The cheapest flight is the 1-stop flight")
        cheapest_one_stop_departure_element.click()
        page.wait_for_load_state("domcontentloaded")
        cheapest_one_stop_return_element.click()
        page.wait_for_load_state("domcontentloaded")
        # Get the url of the page
        url = page.url
        print(url)

        # Close the browser
        browser.close()
        return url, cheapest_one_stop_amount, cheapest_one_departure_airline, cheapest_one_stop_departure_duration, cheapest_one_stop_departure_time, cheapest_one_stop_arrival_time, cheapest_one_stop_return_element, cheapest_one_stop_return_airline, cheapest_one_stop_return_duration, cheapest_one_stop_return_flight_time, cheapest_one_stop_return_arrival_time

#with sync_playwright() as playwright:
 #   run(playwright)

where_from = "cmh"
where_to = "sxm"
departure_date = "07/12/2025"
return_date = "07/19/2025"
max_time = 10

def run_flight_search(where_from, where_to, departure_date, return_date, max_time):
    with sync_playwright() as playwright:
        url = run(playwright, where_from, where_to, departure_date, return_date, max_time)
        return url