def get_summary_statistics(d_data: dict) -> dict:
    t_list = list(d_data.keys())

    n = len(t_list)

    if n > 0:
        min_t = t_list[0]
        max_t = t_list[-1]
        min_value = d_data[min_t]
        max_value = d_data[max_t]
    else:
        min_t = None
        max_t = None
        min_value = None
        max_value = None

    return dict(
        n=n,
        min_t=min_t,
        max_t=max_t,
        min_value=min_value,
        max_value=max_value,
    )
