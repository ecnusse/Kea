Write property for HarmonyOS
=================================

tutorial for uiviewer (UI inspector for HarmonyOS)
-------------------------------------------------------

We use uiviewer for HarmonyOS. The following command will install and launch uiviewer for you.

.. code-block:: bash

    pip install -U uiviewer

    python -m uiviewer

This will start a host server on http://localhost:8000/ by default. You can access this site with a
web browser.


HarmonyOS PDL API 
---------------------------------------------------
We use hmdriver2 for PDL api, which is similar to uiautomator2.

The unique selector in HarmonyOS is **key** or **id** (will be deprecated soon). You can also use **text** and
**description** to target a device.

You can see the usage of hmdriver2 `here <https://github.com/codematrixer/hmdriver2>`_

Here's some examples for HarmonyOS PDL.

.. code-block:: python

    # click a widget that has id "wifi_entry.icon"
    d(id="wifi_entry.icon").click()

    # click a widget that has key "display_settings.title" and text "Display"
    d(key="display_settings.title", text="Display").long_click()

    # Enter "hello" to the widget that has id "url_input_in_search"
    d(id="url_input_in_search").input_text("hello")

Launch Kea for HarmonyOS
----------------------------------------------

You should specify the system of your PC in ``config.yml``. You can see the tutorial for :ref:`yml_confg`.

Here's an example. 

.. code-block:: yaml

    # config.yml

    # Claim the system of the PC is Linux
    env: Linux 

you can specify other args in terminal or in config.yml. Checkout the provided
``config.yml`` for details.

If you specified all the nessary args in config.yml, you can start kea via ``kea -load_config``.
The following example is a fully-configured and can be launched by ``kea -load_config``.

.. code-block:: yaml

    # env: the system of your PC (e.g. windows, macOS, Linux)
    env: Linux

    # system: the target harmonyOS
    system: harmonyOS

    device: 127.0.0.1:5555
    app_path: example/example.hap
    policy: random
    count: 100
    properties: 
        - example/example_hm_property.py