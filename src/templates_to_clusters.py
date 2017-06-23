"""For testing, offsets existing templates."""

import numpy as np

theta = np.pi / 4
R = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta), np.cos(theta), 0],
    [0, 0, 1]])
t = np.array([1, 1, 1]) * 5
s = 0.9


def transform(name: str):
    sedan = np.load('./data/templates/%s.npy' % name)

    sedan_translated = sedan + t
    np.save('./data/test/%s_translated.npy' % name, sedan_translated)

    sedan_scaled = sedan * s
    np.save('./data/test/%s_scaled.npy' % name, sedan_scaled)

    sedan_rotated = sedan.dot(R)
    np.save('./data/test/%s_rotated.npy' % name, sedan_rotated)

    sedan_obscured = sedan[sedan[:, 0] > 0] + 1
    np.save('./data/test/%s_obscured.npy' % name, sedan_obscured)

    sedan += t
    sedan *= s
    sedan_transformed = sedan.dot(R)
    np.save('./data/test/%s_transformed.npy' % name, sedan_transformed)

transform('sedan')
