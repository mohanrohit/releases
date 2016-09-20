# releases

## requirements

  - application exists at /releases/v1

## use-cases

  when users visit:
    /releases/v1 => see a list of applications defined
    /releases/v1/<slug> => see a page for the given application with links to release notes for all versions
    /releases/v1/<slug>/<version> => see the release notes for the given application and version in sections (like the actual doc), with links to edit each section
    /releases/v1/<slug>/<version>?section=<section> => view and edit the selected section

## database tables

  - application
    id (int)
    slug (string)
    name (string)
    timestamp (datetime); when it was created

  - version
    id (int)
    application_id (int, fk)
    spec (string); major.minor.patch.build format
    timestamp (datetime); when it was created

  - release_notes
    id (int)
    version_id (int, fk)
    timestamp

  - release_notes_sections
    id (int)
    release_notes_id (int, fk)
    name (string)
    