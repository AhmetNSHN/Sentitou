import json

def test_naive_bayes(testdoc, logprior, loglikelihood, V):
    classes = [0, 1, 2, 3, 4]
    # Initialize logpost[ci]: stores the posterior probability for class ci
    logpost = [None] * len(classes)
    print(testdoc)
    for ci in classes:
        sumloglikelihoods = 0

        for word in testdoc:
            if word in V:
                # This is sum represents log(P(w|c)) = log(P(w1|c)) + log(P(wn|c))
                sumloglikelihoods += loglikelihood[word][ci]

        # Computes P(c|d)
        logpost[ci] = logprior[ci] + sumloglikelihoods

    # Return the class that generated max ĉ
    return logpost.index(max(logpost))


def predict(testing):
    with open('aspect_based_data/logprior.json', "r") as f:
        logprior = json.load(f)

    with open('aspect_based_data/Vocabulary.json', "r") as f:
        V = json.load(f)

    with open("aspect_based_data/Database.json", "r") as f:
        loglikelihood = json.load(f)

    counter = 0
    for x in testing:
        result = test_naive_bayes(x[0], logprior, loglikelihood, V)
        print(f"class:{x[1]} -> calculated as: {result}")
        if x[1] == str(result):
            counter += 1

    print(f"Accuracy: {counter/len(testing)}")
