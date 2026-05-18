# Test Quality

Prefer tests that:

- prove user-visible behaviour
- fail for the right reason
- use realistic inputs
- avoid sleeps and timing guesses
- keep fixtures small
- name the risk they cover

Weak tests:

- only assert that a function was called
- mirror implementation details
- require network by default
- pass without checking the important result

