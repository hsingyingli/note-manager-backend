# Note-manager
---
## Table of Content

* [Description](#description)
* [Development Pipline](#development-pipline)
* [Folder Structure](#folder-structure)

## Description
QuickNote is a fast and feature-rich note-taking application built with FastAPI in Python. 
It's designed to help users capture, organize, and manage their thoughts, ideas, and information seamlessly. 
With QuickNote, you can create and edit notes in Markdown, categorize them, set reminders, and collaborate with others.

## Development Pipline
### Overview
```
Developer -- Push to Github --> Github -- Webhook --
--> Jenkins
    -- Test
    -- Check Code Quality --> SonarQube
    -- Publish Docker Image --> Dockerhub
    -- Deploy --> AWS
```
### Git
```
                    feature/*
                   /        \
        development---------------- 
       /                            \
main --------------------------------
```

## Folder Structure
```
```

