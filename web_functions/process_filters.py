tech_df = None
exp_df = None

def refresh_filters(technologies, experience):
    global tech_df, exp_df
    tech_df = technologies
    tech_df = tech_df.sort_values(by="technology")
    exp_df = experience

def get_filters_options(filters):
    technologies = [{"index": str(idx), "value": row["technology"]} for idx, row in tech_df.iterrows()]
    experience = [{"index": str(idx), "value": row["experience"]} for idx, row in exp_df.iterrows()]

    dropdown_data = {
        "technology": [{"index": "0", "value": "Any technology"}] + technologies,
        "experience": [{"index": "0", "value": "Any experience"}] + experience,
        "work_format": [{"index": "", "value": "Any work format"},
                        {"index": "Remote", "value": "Remote"},
                        {"index": "Office", "value": "Office"},
                        {"index": "Mixed", "value": "Mixed"}]
    }

    default_values = {"technology": "0", "experience": "0", "work_format": ""}

    return {key: dropdown_data[key] for key in filters}, {key: default_values[key] for key in filters}

def get_filters_values(filters):
    technology = 0 if "technology" not in filters else int(filters["technology"])
    experience = 0 if "experience" not in filters else int(filters["experience"])
    work_format = None if "work_format" not in filters else filters["work_format"]

    return technology, experience, work_format
