# Code repository and version history

## Latest source code:
- Diverse-Assign v1.0.1
    - First production release outside of BETA.
    - Enhancements
        - *Software*
            - Improved accuracy and precision consistency across different data topologies.
            - Auto-scaling of optimisation iterations and sensitivity to changes in diversity measured during swapsping. 
            - These two are auto-scaled, to ensure the same sensitivity to diversity across different number of features and number of groups to assign. 


## Code versioning convention
- Every version of the source code has an "a" and "b" version.
    - "a" version is the code for production release.
    - "b" version is the code used for development.
        - "b" version has additional code used in:
            - debugging and tracing
            - may have additional development features. E.g. Generating test output for statiistical analysis 

## Notes for compiling
- Source codes can be directly run as python script or compiled.
- Reference python and package versions are indicated at the top of the code.
- To compile: *Diverse-Assign* is designed to be compiled using [PyInstaller](https://pyinstaller.org)

## Full source code version history

### v.1.0.1 (Production)
- First production release outside of BETA.
- Enhancements
    - *Software*
        - Improved accuracy and precision consistency across different data topologies.
        - Auto-scaling of optimisation iterations and sensitivity to changes in diversity measured during swapsping. 
        - These two are auto-scaled, to ensure the same sensitivity to diversity across different number of features and number of groups to assign. 

### v.0.3.0 BETA (Pre-production)
- BETA pre-production release.
- Enhancements
    - *Software*
        - Smaller file size of compiled app. (10x smaller). App's BLAS binary now compiled using OpenBLAS library.  
        - Overhaul diversity score calculation functions. Improved accuracy, time and memory performance.
        - Complete re-design of main algorithms. Group assigning can now achieve maximum diversity convergence. Variance in diversity score of sassignments greatly reduced. Also, improvements to time and memory performance.
        - Added constraint satisfaction to prohibit formation of groups with homogenous feature
        - Added heurisitic to relax constraint of prohibiting homogenous feature. Heuristic will relax if this constraint is not possible.
        - Various other perfomance optimisations.
        - Added alogirthm to modulate importance of features using weights. Still in development. Algorithm is de-activated in this version.
        - "b" version include "MegaTester" mode.
            - "MegaTester" mode used for experimenting various algorithms and settings.
            - Generates output for statisitical analysis.
            - "b" version used for [pilot study](https://github.com/joseph-liew/Diverse-Assign/tree/main/site/pilot_study) of Diverse-Assign's performance. Detailed abstract in [technical abstract](https://github.com/joseph-liew/Diverse-Assign/tree/main/tech_abstract).
- Issues fixed:
    - *UI*
        - Fixed de-syncing of UI's diversity score that occur under certain conditions
        - Fixed de-syncing of UI's job progress percentage that occur under certain conditions
  
### v.0.2.3 BETA (Production)
- BETA release of Diverse-Assign 
