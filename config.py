class Config:
    letters = 'abcdefg'
    numbers = '12345'
    orientations = 'frbl'
    actions = 'frl'

    edges = {
        ('a1', 'a2'): -100.,
        ('a4', 'b4'): -100.,
        ('a3', 'b3'): -100.,
        ('c2', 'd2'): -100.,
        ('c1', 'd1'): -100.,
        ('a2', 'b2'): -100.,
        ('b2', 'c2'): -100.,
    }
    edge_default_weight = -1.0
