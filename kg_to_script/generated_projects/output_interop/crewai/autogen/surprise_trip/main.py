import asyncio

from team import (
    personalized_activity_planner,
    restaurant_scout,
    itinerary_compiler,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution
        # ==================================================
        # Workflow Step: task_personalized_activity_planning_task
        # Workflow Edge: task_personalized_activity_planning_task -> task_restaurant_scenic_location_scout_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_personalized_activity_planning_task")
        print("=" * 80)

        task_prompt = """Research and find cool things to do at {destination}. Focus on activities and events that match the traveler's interests and age group. Utilize internet search tools and recommendation engines to gather the information. """
        # Execute via the assigned agent: personalized_activity_planner
        result = await personalized_activity_planner.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_restaurant_scenic_location_scout_task
        # Workflow Edge: task_restaurant_scenic_location_scout_task -> task_itinerary_compilation_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_restaurant_scenic_location_scout_task")
        print("=" * 80)

        task_prompt = """Find highly-rated restaurants and dining experiences at {destination}. Recommend scenic locations and fun activities that align with the traveler's preferences. Use internet search tools, restaurant review sites, and travel guides. """
        # Execute via the assigned agent: restaurant_scout
        result = await restaurant_scout.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_itinerary_compilation_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_itinerary_compilation_task")
        print("=" * 80)

        task_prompt = """Compile all researched information into a comprehensive day-by-day itinerary for the trip to {destination}. Ensure the itinerary integrates flights, hotel information, and all planned activities and dining experiences. """
        # Execute via the assigned agent: itinerary_compiler
        result = await itinerary_compiler.run(task=task_prompt)

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