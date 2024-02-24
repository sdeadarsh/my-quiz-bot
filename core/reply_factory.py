from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    # Example validation: check if the answer is not empty
    if not answer:
        return False, "Answer cannot be empty."
        # Example storage: store the answer in the session
    session_key = f"question_{current_question_id}_answer"
    session[session_key] = answer
    session.save()

    return True, ""  # Return success


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    # Find the index of the current question
    current_question_index = None
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        if question["question_text"] == current_question_id:
            current_question_index = i
            break

    # If current_question_id is not found, start from the first question
    if current_question_index is None:
        return PYTHON_QUESTION_LIST[0]["question_text"], PYTHON_QUESTION_LIST[0]

    # If there are more questions left, return the next question
    if current_question_index < len(PYTHON_QUESTION_LIST) - 1:
        next_question = PYTHON_QUESTION_LIST[current_question_index + 1]
        return next_question["question_text"], next_question
    else:
        return None, None  # No more questions left


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    # Iterate through the questions and compare user's answers
    for question in PYTHON_QUESTION_LIST:
        session_key = f"question_{question['question_text'].replace(' ', '_')}_answer"
        user_answer = session.get(session_key)
        correct_answer = question["answer"]

        if user_answer == correct_answer:
            score += 1

    # Generate final response message
    final_response = f"Your final score is {score}/{total_questions}."
    if score == total_questions:
        final_response += " Congratulations, you got all questions correct!"
    elif score == 0:
        final_response += " Better luck next time!"
    else:
        final_response += " Keep up the good work!"
    return "dummy result"
