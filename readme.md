Bencode.cy
============

A fast bencode implementation in Cython that supports Python 3. It uses Cython's pure Python syntax.

.. image:: https://img.shields.io/pypi/l/bencode.cy.svg
    :alt: PyPI License
    :target: https://pypi.org/project/bencode.cy/


Install
-------


.. code-block:: bash

    pip install bencode.cy


Speed benchmark
-------


<table>
  <thead>
    <tr>
      <th>Name (time in us)<br>(Kops/s)</th>
      <th>Rounds</th>
      <th>Iterations</th>
      <th>Min</th>
      <th>Max</th>
      <th>Mean</th>
      <th>StdDev</th>
      <th>Median</th>
      <th>IQR</th>
      <th>Outliers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>test_bencode_benchmark<br><span style="color: green;">295.5083 (1.0)</span></td>
      <td>64000</td>
      <td>1</td>
      <td><span style="color: green;">3.1660 (1.0)</span></td>
      <td>96.9160 (2.11)</td>
      <td><span style="color: green;">3.3840 (1.0)</span></td>
      <td>0.4740 (1.48)</td>
      <td><span style="color: green;">3.3750 (1.0)</span></td>
      <td><span style="color: green;">0.0420 (1.0)</span></td>
      <td>718;9493</td>
    </tr>
    <tr>
      <td>test_bdecode_benchmark<br><span style="color: red;">270.3499 (0.91)</span></td>
      <td>51393</td>
      <td>1</td>
      <td>3.4160 (1.08)</td>
      <td><span style="color: green;">45.8750 (1.0)</span></td>
      <td>3.6989 (1.09)</td>
      <td><span style="color: green;">0.3211 (1.0)</span></td>
      <td>3.6670 (1.09)</td>
      <td><span style="color: green;">0.0840 (2.00)</span></td>
      <td>675;1780</td>
    </tr>
    <tr>
      <td>test_bencode_pyx_benchmark<br><span style="color: red;">217.9582 (0.74)</span></td>
      <td>64692</td>
      <td>1</td>
      <td>3.6660 (1.16)</td>
      <td><span style="color: red;">1,718.6250 (37.46)</span></td>
      <td>4.5880 (1.36)</td>
      <td><span style="color: red;">16.2727 (50.67)</span></td>
      <td>3.8750 (1.15)</td>
      <td>0.0830 (1.98)</td>
      <td>191;7556</td>
    </tr>
    <tr>
      <td>test_bdecoder_pyx_benchmark<br><span style="color: red;">194.6135 (0.66)</span></td>
      <td>66481</td>
      <td>1</td>
      <td><span style="color: red;">4.7910 (1.51)</span></td>
      <td>64.1660 (1.40)</td>
      <td><span style="color: red;">5.1384 (1.52)</span></td>
      <td>0.4587 (1.43)</td>
      <td><span style="color: red;">5.1250 (1.52)</span></td>
      <td><span style="color: red;">0.1240 (2.95)</span></td>
      <td>970;1778</td>
    </tr>
  </tbody>
</table>
Tested use python3.11.13 on MacBook Air M2 with macOS 26.01 in 2025-10

Usage
-----


.. code-block:: python

    from bencoder import bencode, bdecode
    
    assert bencode("WWWWWW") == b'6:WWWWWW'
    assert bencode(233) == b'i233e'
    
    with open("debian-8.3.0-amd64-netinst.iso.torrent", "rb") as f:
        torrent = bdecode(f.read())
        print(torrent[b'announce'])
    

ChangeLog
----------

Version 1.1.0
~~~~~~~~~~~~~~~

+ init