.. _bug_report_tutorial:

How to read bug reports
=======================

.. image:: ../../../images/BugReport.png
            :align: center

|

The above image is a bug report of Omninotes, it's search bar disappeared after the user rotate the screen.
So it violate the ``search_bar_should_exist_after_rotation`` property.

After the testing, You can see a ``bug_report.html`` in the output folder under your output path.
You can use the browser (Google Chrome, Firefox, etc.) to open ``bug_report.html`` file in the output directory.

The line at the top of the report record the screenshot of every UI states during the testing process,
which can help you identify and reproduce the bug.
Under each screenshot, you can see the event index and the event type (e.g., click, long click) that executed on the UI state.
The table below shows a property violation list, it contains ``precondition link``, ``interaction link`` and ``postcondition link`` of
every property violation situation. Click the link will jump to the corresponding screenshots,
to help you understand what happened at that moment.