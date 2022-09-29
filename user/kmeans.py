import random
import matplotlib.pyplot as plt


def kmeans(data_set):

    participants = []
    chats = []

    for data in data_set:
        participants += [data[0]]
        chats += [data[1]]

    for i in range(len(data_set)):
        data_set[i] += [0]

    centroids = [[random.choice(participants), random.choice(chats)], [random.choice(participants), random.choice(chats)]]

    iterations = 0
    old_centroids = None

    while not should_stop(old_centroids, centroids, iterations):
        old_centroids = centroids
        iterations += 1
        get_labels(data_set, centroids)
        centroids = get_centroids(old_centroids, data_set)

    print(data_set)

    colors = []
    participants = []
    chats = []
    for data in data_set:
        participants += [data[0]]
        chats += [data[1]]
        colors += ['red' if data[2] == 0 else 'blue']

    print(participants)
    print(chats)
    print(colors)

    return participants, chats, colors


def get_centroids(old_centroids, data_set):

    first_cluster_participants = []
    first_cluster_chats = []
    second_cluster_participants = []
    second_cluster_chats = []

    for data in data_set:
        if data[2] == 0:
            first_cluster_participants += [data[0]]
            first_cluster_chats += [data[1]]
        else:
            second_cluster_participants += [data[0]]
            second_cluster_chats += [data[1]]

    centroid = []

    if len(first_cluster_participants) == 0:
        centroid += [old_centroids[0]]
    else:
        centroid += [[sum(first_cluster_participants)/len(first_cluster_participants),
                      sum(first_cluster_chats)/len(first_cluster_chats)]]

    if len(second_cluster_participants) == 0:
        centroid += [old_centroids[1]]
    else:
        centroid += [[sum(second_cluster_participants) / len(second_cluster_participants),
                      sum(second_cluster_chats) / len(second_cluster_chats)]]

    return centroid


def should_stop(old_centroids, centroids, iterations):
    if iterations > 500: return True
    return old_centroids == centroids


def get_labels(data_set, centroids):

    i = 0

    for data in data_set:
        first_distance = ((centroids[0][0]-data[0])**2 + (centroids[0][1]-data[1])**2)**0.5
        second_distance = ((centroids[1][0]-data[0])**2 + (centroids[1][1]-data[1])**2)**0.5
        if first_distance < second_distance:
            data_set[i][2] = 0
        else:
            data_set[i][2] = 1
        i += 1

    return data_set


if __name__=="__main__":
    kmeans()