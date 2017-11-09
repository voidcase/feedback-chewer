def plot_vocab(column,df):
    values = df[column].values
    vectorizer = CountVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(values).toarray()
    featurenames = np.asarray(vectorizer.get_feature_names())
    tfidf_frame = pd.DataFrame(matrix, columns=featurenames)
    frequencylist = np.zeros(shape=(len(featurenames)))
    i = 0
    for column in tfidf_frame:
        s = sum(tfidf_frame[column])
        frequencylist[i] = s
        i += 1
        if (s > 500):
            print(column)
    plt.plot(sorted(frequencylist, reverse=True))
    plt.show()