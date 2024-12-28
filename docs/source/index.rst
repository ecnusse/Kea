Kea: a property-based testing tool for mobile apps
============================================================

Kea is a testing tool based on the idea of property-based testing for finding functional bugs in Android apps.
Given a set of properties, Kea automatically generates test cases to check the properties. 
When a property is violated, Kea generates a bug report that shows the bug's behavior.
Users can use Kea in the following steps:

1. Specify properties for the app under test.
A property is the expected behavior of the app under certain conditions.
Users can specify properties based on the app's specification, documentation, test cases, or bug reports.
Currently, Kea supports specifying properties in Python with multiple APIs.


2. Run Kea with the properties and the app under test. 
Kea will automatically generate test cases to explore the app.
When the precondition of a property is satisfied, Kea will execute the interaction scenario of the property and check the postcondition.
If the postcondition is violated, Kea will generate a bug report.


Contents
--------

.. toctree::
   :caption: PART1: QUICK START

   part-quickStart/androidSDK
   part-quickStart/first_property

.. toctree::
   :caption: PART2: USER MANUEL

   part-keaUserManuel/introduction
   part-keaUserManuel/api
   part-keaUserManuel/tutorial
   part-keaUserManuel/options
   part-keaUserManuel/stateful testing

.. toctree::
   :caption: PART3: KEA FOR HarmonyOS

   part-keaForHarmonyOS/harmonyos_setup
   part-keaForHarmonyOS/harmonyos_api

.. toctree::
   :caption: PART4: APPENDIX

   part-Appendix/trophies
   part-Appendix/PDL

.. automodule:: kea.start
   :members:
   :undoc-members:
   :show-inheritance: