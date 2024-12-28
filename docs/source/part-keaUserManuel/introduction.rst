Introduction
====================================

Kea introduces a general and practical testing technique based on property-based testing(PBT)
for finding functional bugs in Mobile Apps. Given an app and some properties of interest (specified by a human tester),
Kea automatically explores the app to validate the property. If the property is violated, Kea will output a bug report, which contains some GUI tests illustrating the violation.
Specifically, to support the application of property-based testing, Kea provides

(1) A Python-based property description language to help users specify the desired app properties.

(2) Two exploration strategies to generate a large number of GUI tests for validating the properties.

.. toctree::

   introduction/procedure
   introduction/Advantage
   introduction/BugReport