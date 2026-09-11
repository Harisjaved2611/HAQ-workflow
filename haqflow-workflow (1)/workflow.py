
from models import ActionItem


def generate_action_plan(match_result):

    tasks = []

    for program in match_result.get("programs", []):

        program_id = program.get("program_id")
        program_name = program.get("program_name")

        missing_evidence = program.get(
            "missing_evidence",
            []
        )

        for index, evidence in enumerate(missing_evidence):

            task = ActionItem(
                id=f"{program_id}_evidence_{index + 1}",
                title=f"Upload {evidence}",
                priority="HIGH",
                status="PENDING",
                related_program_id=program_id,
                related_program_name=program_name,
                source="missing_evidence"
            )

            task.validate()
            tasks.append(task)

        application_steps = program.get(
            "application_steps",
            []
        )

        for index, step in enumerate(application_steps):

            task = ActionItem(
                id=f"{program_id}_application_{index + 1}",
                title=step,
                priority="MEDIUM",
                status="PENDING",
                related_program_id=program_id,
                related_program_name=program_name,
                source="application_steps"
            )

            task.validate()
            tasks.append(task)

    return tasks


def update_task_status(tasks, task_id, new_status):

    valid_statuses = {
        "PENDING",
        "IN_PROGRESS",
        "COMPLETED",
        "BLOCKED"
    }

    if new_status not in valid_statuses:
        raise ValueError(
            f"Invalid status: {new_status}"
        )

    for task in tasks:

        if task.id == task_id:

            task.status = new_status
            task.validate()

            return task

    raise ValueError(
        f"Task with id '{task_id}' was not found."
    )


def calculate_progress(tasks):

    if not tasks:
        return 0

    completed = 0

    for task in tasks:

        if task.status == "COMPLETED":
            completed += 1

    progress = (completed / len(tasks)) * 100

    return round(progress, 2)


def get_pending_tasks(tasks):

    pending_tasks = []

    for task in tasks:

        if task.status == "PENDING":
            pending_tasks.append(task)

    return pending_tasks


def generate_follow_up(tasks):

    pending_tasks = get_pending_tasks(tasks)

    follow_ups = []

    for task in pending_tasks:

        follow_up = {
            "task_id": task.id,
            "title": task.title,
            "priority": task.priority,
            "program_id": task.related_program_id,
            "program_name": task.related_program_name,
            "message": f"Reminder: {task.title}"
        }

        follow_ups.append(follow_up)

    return follow_ups


def generate_human_handoff(
    case_id,
    user_situation,
    match_result,
    tasks,
    unresolved_questions=None
):

    if unresolved_questions is None:
        unresolved_questions = []

    completed_evidence = []
    missing_evidence = []
    recommended_actions = []

    for task in tasks:

        if task.source == "missing_evidence":

            if task.status == "COMPLETED":
                completed_evidence.append(task.title)

            elif task.status in {
                "PENDING",
                "IN_PROGRESS",
                "BLOCKED"
            }:
                missing_evidence.append(task.title)

        if task.status in {
            "PENDING",
            "BLOCKED"
        }:
            recommended_actions.append(task.title)

    matched_programs = []

    for program in match_result.get("programs", []):

        matched_programs.append({
            "program_id": program.get("program_id"),
            "program_name": program.get("program_name"),
            "match_level": program.get("match_level"),
            "score": program.get("score")
        })

    handoff = {
        "case_id": case_id,
        "user_situation": user_situation,
        "matched_programs": matched_programs,
        "completed_evidence": completed_evidence,
        "missing_evidence": missing_evidence,
        "unresolved_questions": unresolved_questions,
        "recommended_next_actions": recommended_actions,
        "progress": calculate_progress(tasks)
    }

    return handoff
