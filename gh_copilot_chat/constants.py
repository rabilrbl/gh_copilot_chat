HEADERS = {
    "Accept": "application/vnd.github.merge-info-preview+json,application/vnd.github.shadow-cat-preview+json,application/vnd.github.echo-preview+json,application/vnd.github.vixen-preview+json,application/vnd.github.antiope-preview+json,application/vnd.github.comfort-fade-preview+json,application/vnd.github.starfox-preview+json,application/vnd.github.doctor-strange-preview+json,application/json",
    "Accept-Encoding": "gzip",
    "Connection": "Keep-Alive",
    "Content-Type": "application/json; charset=UTF-8",
    "Copilot-Integration-Id": "copilot-mobile-android",
    "GraphQL-Features": "merge_queue,project_next_field_configuration,issue_types,issues_close_state,project_next_recent_connection,file_level_commenting",
    "Host": "api.githubcopilot.com",
    "User-Agent": "GitHub/1.161.0 (com.github.android; build:786; Android 13; Pixel 5)",
    "X-GitHub-Api-Version": "2023-07-07",
}

GH_COPILOT_CHAT_API_HOST = "https://api.githubcopilot.com/github/chat"

GH_COPILOT_THREADS = f"{GH_COPILOT_CHAT_API_HOST}/threads"
