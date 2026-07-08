import asyncio

from team import (
    travel_agent,
    travel_analyzer,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)
from autogen_agentchat.messages import BaseChatMessage, TextMessage

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution.
        #
        # `history` accumulates every step's real conversation so far and is
        # threaded into each subsequent step's .run() call. Without this,
        # each step only ever sees its own task prompt in isolation - later
        # steps (e.g. "review the draft") have no way to see what an earlier
        # step (e.g. "draft the posting") actually produced.
        history: list[BaseChatMessage] = []
        # ==================================================
        # Workflow Step: task_outbound_flight
        # Workflow Edge: task_outbound_flight -> task_return_flight
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_outbound_flight")
        print("=" * 80)

        task_prompt = """Available outboundFlight items will be provided. Select a single outbound flight based on travelForm (departureLocation, arrivalLocation, startDate, endDate) and flightPriority. ALWAYS pass entire date timestamps for departureTime and arrivalTime. Return ids (or flightNumber) and a short reasoning. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: travel_analyzer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await travel_analyzer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_return_flight
        # Workflow Edge: task_return_flight -> task_accommodation_hotels
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_return_flight")
        print("=" * 80)

        task_prompt = """Available returnFlight items will be provided. Select a single return flight based on travelForm and flightPriority. ALWAYS return full flight objects for outbound and return flights and timestamps. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: travel_analyzer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await travel_analyzer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_accommodation_hotels
        # Workflow Edge: task_accommodation_hotels -> task_attraction
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_accommodation_hotels")
        print("=" * 80)

        task_prompt = """Given available hotels and the travelForm (arrivalCityId, hotelPriceRange), select up to 3 hotel options. Ignore 'reviewScore' and extract numeric rating from description/accessibility fields. Provide ids and reasoning. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: travel_analyzer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await travel_analyzer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_attraction
        # Workflow Edge: task_attraction -> task_airbnb_location
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_attraction")
        print("=" * 80)

        task_prompt = """Given a set of attractions for the arrival city and the user's interests, select three attractions, provide brief reasoning, and include price, duration, and rating where available. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: travel_analyzer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await travel_analyzer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_airbnb_location
        # Workflow Edge: task_airbnb_location -> task_accommodation_airbnb
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_airbnb_location")
        print("=" * 80)

        task_prompt = """Search for Airbnb location matches for the arrival city and select up to 3 unique place ids to be used in the subsequent Airbnb search. Provide ids and reasoning. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: travel_analyzer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await travel_analyzer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_accommodation_airbnb
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_accommodation_airbnb")
        print("=" * 80)

        task_prompt = """Given Airbnb search results and travelForm (typeOfPlace, startDate, endDate), select up to 3 Airbnb options, then pick the top result to return. Provide ids and reasoning. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: travel_analyzer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await travel_analyzer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_sync_csv_data
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_sync_csv_data")
        print("=" * 80)

        task_prompt = """Sync data from City CSV (src/data/city-data.csv). Read CSV rows, map columns to CityData, and call mastra.engine.syncRecords to sync City records. This step is executed by the Mastra engine runtime. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: travel_analyzer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await travel_analyzer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        print("\n" + "=" * 80)
        print("DONE")
        print("=" * 80)

    except Exception as e:
        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)
        print(type(e).__name__)
        print(str(e))



if __name__ == "__main__":
    asyncio.run(main())