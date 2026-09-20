Attendance frequency and academic outcome composition
=====================================================

This workflow supports observational studies of education-support usage that
need to distinguish initial engagement, frequency among users, and the
composition of adverse academic outcomes.

The central design principle is to choose exposure groups from sample support
and within-context overlap before inspecting outcome means or p-values.

Recommended workflow
--------------------

1. Construct the study cohort and primary academic outcomes.
2. Add exact academic-result states with
   cmat_analysis.measures.add_academic_outcome_states when administrative
   outcomes matter substantively.
3. Run cmat_analysis.statistics.visit_frequency_support_audit and
   cmat_analysis.statistics.visit_frequency_cut_frontier without outcome
   columns.
4. Record and freeze the grouping decision.
5. Apply it with cmat_analysis.statistics.add_topcoded_visit_group.
6. Inspect pairwise context support with
   cmat_analysis.statistics.visit_group_pair_overlap.
7. Estimate omnibus and all-pair adjusted comparisons with
   cmat_analysis.statistics.fixed_effect_group_comparisons.
8. Summarize outcomes with cmat_analysis.statistics.group_outcome_summary.
9. Describe adverse-result composition and distribution shape with
   cmat_analysis.statistics.outcome_state_composition and
   cmat_analysis.statistics.distribution_profile.
10. Create a visualization-ready signed matrix with
    cmat_analysis.statistics.pairwise_effect_matrix.

Outcome-blind grouping example
------------------------------

.. code-block:: python

   from cmat_analysis.statistics import (
       add_topcoded_visit_group,
       visit_frequency_cut_frontier,
       visit_frequency_support_audit,
   )

   exact_support = visit_frequency_support_audit(
       cohort,
       visits_col="VISITS_CMAT_PERIOD",
       cluster_col="CLASSROOM_ID",
       instructor_col="CLAVEPROFESOR",
   )

   frontier = visit_frequency_cut_frontier(
       cohort,
       visits_col="VISITS_CMAT_PERIOD",
       cluster_col="CLASSROOM_ID",
       min_top_exact=2,
       max_top_exact=10,
   )

   analysis = add_topcoded_visit_group(
       cohort,
       visits_col="VISITS_CMAT_PERIOD",
       top_exact=5,
       include_zero=False,
       output_col="VISIT_GROUP",
   )

The frontier intentionally does not return an automatic optimum. The study must
decide how much frequency resolution is worth the accompanying loss of sample
and within-context overlap.

Clustered fixed-effect comparisons
----------------------------------

.. code-block:: python

   from cmat_analysis.statistics import fixed_effect_group_comparisons

   pairwise, omnibus, model_info = fixed_effect_group_comparisons(
       users,
       group_col="VISIT_GROUP",
       group_order=["1", "2", "3", "4", "5", "6+"],
       outcome_col="Z_GRADE_PRIMARY",
       fixed_effect_col="CLASSROOM_ID",
       cluster_col="CLASSROOM_ID",
       categorical_covariates=["CLAVECARRERA"],
   )

For a binary 0/1 outcome, the same helper estimates a linear-probability model.
Multiply contrasts by 100 to express them in percentage points. A broader
clustering sensitivity can change cluster_col while retaining the same fixed
effect definition.

Academic-result composition
---------------------------

.. code-block:: python

   from cmat_analysis.measures import add_academic_outcome_states
   from cmat_analysis.statistics import outcome_state_composition

   outcomes = add_academic_outcome_states(cohort)

   composition = outcome_state_composition(
       outcomes,
       group_col="VISIT_GROUP_WITH_ZERO",
       group_order=["0", "1", "2", "3", "4", "5", "6+"],
       state_col="ACADEMIC_OUTCOME_STATE_5",
       state_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
   )

The derived conditional columns support administrative-versus-numeric, BV/RT,
BV-only, and RT-only comparisons among non-passing records. These describe how
adverse records are composed; they do not measure engagement, motivation,
knowledge of university procedures, or causal effects of support use.

Scientific boundaries
---------------------

* Attendance frequency is service use, not automatically a treatment dose.
* A non-significant pairwise contrast is not evidence of equivalence.
* Administrative codes can have different institutional meanings.
* Fixed effects and clustered standard errors do not remove unmeasured
  student-level selection.
* When withdrawal can occur before period end, opportunity to accumulate visits
  can differ across final outcome states.


Stacked ridgeline distributions
-------------------------------

For figures that need to show both a continuous outcome distribution and the
composition of categorical final states, first build weighted KDE components:

.. code-block:: python

   from cmat_analysis.statistics import mixture_component_density
   from cmat_analysis.visualization import plot_stacked_ridgeline

   density = mixture_component_density(
       outcomes,
       group_col="VISIT_GROUP_WITH_ZERO",
       group_order=["0", "1", "2", "3", "4", "5", "6+"],
       outcome_col="Z_GRADE_PRIMARY",
       component_col="ACADEMIC_OUTCOME_STATE_5",
       component_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
   )

   ax = plot_stacked_ridgeline(
       density,
       group_order=["0", "1", "2", "3", "4", "5", "6+"],
       component_order=["pass", "numeric_nonpass", "BV", "RT", "BA"],
       summary=group_summary,
   )

Within each attendance group all components use the same kernel bandwidth.
Component densities are weighted by the full group size, so their areas recover
the observed state shares and their sum is the total group density. This is
preferable to colouring arbitrary x-axis segments because the colours remain
tied to the actual observations contributing to each part of the distribution.
