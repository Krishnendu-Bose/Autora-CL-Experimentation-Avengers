# Closed-loop model discovery

In this challenge, you will implement a theorist that can discover equations from data. The theorist should be able to
fit equations to data and predict new data points using the discovered equations. The theorist should be able to recover
at least two ground truth models from the benchmarking data.

## Grading

- Due date: **August 30**
- Submission: Through ``Stud.IP -> Tasks -> Equation Discovery Challenge``

The grading is independent of the outcome of the benchmarking challenge.

The following points will be provided:

- A demonstration of the theorist in the ``doc/Basic Usage.ipynb``:
    - 2 points: Demonstrating how to use the theorist for fitting
    - 2 points: Demonstrating how to use the theorist for predicting
    - 2 points: Demonstrating how to obtain the equation fit by the theorist
    - 4 points: Demonstrating that the theorist can recover at least two ground truth models. (*Hint: You could use the
      benchmarking part of the notebook below as a starting point*).
- The documentation of the theorist in ``doc/index.md`` must speak to the following information:
    - 2 points: Search Algorithm: a description of the search algorithm, and how the goodness of the equation was
      determined?
    - 2 points: Search Space: which search space was used and how was the search otherwise constrained?
- 2 points: The code contains at least two useful unit tests for the theorist method (either doc tests or separate
  tests)
- 1 point: the contributors used issues to track bugs and work on features.
- 1 point: the contributors used (helpful) code reviews for their PRs.
- 1 point: Unit tests are automatically executed when a pull request is created.
- 1 point: The documentation is hosted automatically.

Finally, teams must outline the contributions of each team member in their submission
on ``Stud.IP -> Tasks -> Equation Discovery Challenge``.

In total, you can obtain 20 points.