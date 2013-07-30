Workflow
==========================
Concept
--------------------------
The workflows module takes care of the statuses and access rights. Imagine we have the following workflow:

    - Chief editor assigns the task to an editor and a writer. Chief editor initially creates the task.
    - Editor reviews the work done by writer and reports to chief editor.
    - Writer writes an article (fills it with content). When writer has done his work he reports to editor assigned
      that the task is ready (for a review).
    - Editor reviews the article, decide whether it's ready to be published and reports to the chief editor that
      article is ready and can be published.
    - Chief editor publishes the article.

Implementation
--------------------------
Our news model (only the most important fields, related to the workflow are mentioned):

    - Title (and some other fields that are not important for the workflow)
    - Author
    - Editor
    - Chief editor
    - Date published
    - Status (added by the workflow module)

Workflow statuses:

    - New
    - Draft (work in progress)
    - Ready (ready for a review)
    - Reviewed (can be published)
    - Published

Users:

    Author and Editor are Django admin Users with different rights. In order to have the rights structured, User
    groups were made. As for now we have two user groups (we can have more):

        - Writers
        - Editors
        - Chief editors

    Writers have the following rights:

        - news | News item | Can change News item
        - news | News item | Can change status to draft
        - news | News item | Can change status to new
        - news | News item | Can change status to ready

    Editors have the following rights:

        - news | News item | Can change News item
        - news | News item | Can change author
        - news | News item | Can change status to draft
        - news | News item | Can change status to new
        - news | News item | Can change status to ready
        - news | News item | Can change status to reviewed

    Chief editors have the following rights:

        - news | News item | Can add News item
        - news | News item | Can change author
        - news | News item | Can change chief editor
        - news | News item | Can change editor
        - news | News item | Can change News item
        - news | News item | Can change status to draft
        - news | News item | Can change status to new
        - news | News item | Can change status to published
        - news | News item | Can change status to ready
        - news | News item | Can change status to reviewed
        - news | News item | Can delete News item

All writers belong to User group `Writers`. All editors belong to User group `Editors`. All chief editors belong to
group `Chief editors`.

The process:

    - Chief editors (or someone else who has rights to create a news item with status `New`) logs into the Django
      admin and creates a new News item, fills in the fields (chooses the `Author`, `Editor` and `Chief editor`
      responsible).
    - Chosen editor and writer gets an e-mail notification (a News item has been assigned to them).
    - Chosen writer logs into the Django admin and makes changes. Once writer finishes writing the News item, he
      changes its' status to `Ready`.
    - Chosen editor gets an e-mail notification (Status of an News item he is an editor for has been set to `Ready`).
    - Editor logs into the Django admin, reviews the News item and if it's acceptable sets its' Status to `Reviewed`.
    - Chief editor gets a notification about the News item ready to be published (reviewed by editor) and publishes
      the News item. Only after the News item has been set to `Published` it will appear in the News listings or News
      feeds in the front-end.
