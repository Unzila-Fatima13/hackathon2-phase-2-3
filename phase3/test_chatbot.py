# Test the Task Chatbot

def test_chatbot():
    import json
    import os

    # Import our chatbot
    from chatbot import TaskChatbot

    # Create a test instance
    bot = TaskChatbot()

    # Clean up any existing test data
    if os.path.exists('test_tasks.json'):
        os.remove('test_tasks.json')

    # Override the tasks file for testing
    bot.tasks_file = 'test_tasks.json'
    bot.tasks = []

    # Test adding a task
    response = bot.add_task("Buy groceries")
    assert "Added task: 'Buy groceries'" in response

    # Test adding another task
    response = bot.add_task("Walk the dog")
    assert "Added task: 'Walk the dog'" in response

    # Test listing tasks
    response = bot.list_tasks()
    assert "Buy groceries" in response
    assert "Walk the dog" in response

    # Test completing a task
    response = bot.complete_task(1)
    assert "Completed task: 'Buy groceries'" in response

    # Test deleting a task
    response = bot.delete_task(2)
    assert "Deleted task: 'Walk the dog'" in response

    # Verify the task was removed and only completed task remains
    response = bot.list_tasks()
    # Should have 1 completed task remaining
    assert len(bot.tasks) == 1
    assert bot.tasks[0]['completed'] == True

    print("All tests passed!")

if __name__ == "__main__":
    test_chatbot()