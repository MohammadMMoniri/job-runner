from fastapi import FastAPI
from mongoengine import connect, Document, StringField, DictField, signals
from enum import Enum

from controllers import JobInput
from models import Job
import asyncio

app = FastAPI()


@app.post("/jobs")
async def create_job(job: JobInput):
    # Run linting checks on the code
    lint_errors = []
    # if job.language == ProgrammingLanguage.python:
    #     lint_errors = run_flake8_linter(job.code)
    # elif job.language == ProgrammingLanguage.javascript:
    #     lint_errors = run_eslint(job.code)
    # elif job.language == ProgrammingLanguage.java:
    #     lint_errors = run_checkstyle(job.code)

    if lint_errors:
        return {"message": "Linting errors found", "errors": lint_errors}

    # Create a new instance of the Job model with the received data
    new_job = Job(
        code=job.code,
        scheduling=job.scheduling,
        base_image=job.base_image,
        environments=job.environments,
        language=job.language.value,  # Store the enum value as string
    )

    # Save the job to MongoDB
    await new_job.save()
    asyncio.create_task(check_job, [new_job])
    # Return a response
    return {"message": "Job created successfully"}


def check_job(job: Job, **kwargs):
    # Run the code in a container and check if it executes successfully
    container = docker_client.containers.run(
        job.base_image,
        command=job.code,
        environment=job.environments,
        detach=True,
    )

    exit_code = container.wait()["StatusCode"]
    if exit_code != 0:
        # Handle code execution failure
        print("Code execution failed!")

    # Cleanup the container
    container.remove(force=True)


# signals.post_save.connect(check_job, sender=Job, )


@app.post("/run_job/{job_id}")
def run_job(job_id: str):
    # Retrieve the code from the database or any other data source based on the code_id
    code = Job.retrieve_job_by_id(job_id)

    # Run the code in a Docker container
    container = docker_client.containers.run(code.base_image, command=code, detach=True)

    # Wait for the container to finish executing the code
    container.wait()

    # Get the container logs
    logs = container.logs().decode("utf-8")

    # Remove the container
    container.remove(force=True)

    return {"result": logs}
