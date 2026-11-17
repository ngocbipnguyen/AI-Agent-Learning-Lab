def filter_news(df, topic, number_of_news):
    if topic != "Tất cả":
        filtered_df = df[df["Lĩnh vực"] == topic]
    else:
        filtered_df = df

    return filtered_df.head(number_of_news)