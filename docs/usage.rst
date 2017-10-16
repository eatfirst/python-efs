=====
Usage
=====

To use EatFirst fs + flask wrapper in a project:

.. code-block:: python

    import efs

    # There is no need to initialise it because it will always the current app.
    fs = efs.get_filesystem()
    fs.upload('a/file.txt', open('/tmp/file.txt', 'rb'))
