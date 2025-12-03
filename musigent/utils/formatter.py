import pandas as pd

def flatten_dict(d, parent_key='', sep=' → '):
    """
    Flattens deeply nested dictionaries into a flat dict
    suitable for table display.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def result_to_dataframe(result_dict):
    """
    Converts a full Musigent result (plan, draft, evaluation, time)
    into a clean Pandas DataFrame for Kaggle/Colab display.
    Forces left-to-right text direction for all values.
    """
    flat = flatten_dict(result_dict)

    # force LTR + left alignment to avoid RTL auto-detection
    flat_ltr = {
        k: f"<div style='direction:ltr; text-align:left;'>{v}</div>"
        for k, v in flat.items()
    }

    df = pd.DataFrame(flat_ltr.items(), columns=["Field", "Value"])
    return df


def result_to_sections(result_dict):
    """
    Returns a dictionary of dataframes, one per section,
    ideal if you want separate tables (Plan, Draft, Evaluation).
    """
    sections = {}
    for key, value in result_dict.items():
        if isinstance(value, dict):
            df = pd.DataFrame(value.items(), columns=["Key", "Value"])
            sections[key.upper()] = df
    return sections
