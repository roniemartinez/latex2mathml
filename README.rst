|version|\ |license|\ |status|

latex2mathml
============

Pure Python library for LaTeX to MathML conversion.

Usage
-----

.. code:: python

    import latex2mathml.converter

    latex_input = "<your_latex_string>"
    mathml_output = latex2mathml.converter.convert(latex_input)

Examples
--------

Identifiers, Numbers and Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <table>

::

    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">x</pre></td>
        <td valign="top"><pre lang="html">

<math> <mrow> <mi>x</mi> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">xyz</pre></td>
        <td valign="top"><pre lang="html">

<math> <mrow> <mi>x</mi> <mi>y</mi> <mi>z</mi> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">3</pre></td>
        <td valign="top"><pre lang="html">     

<math> <mrow> <mn>3</mn> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">444</pre></td>
        <td valign="top"><pre lang="html">     

<math> <mrow> <mn>444</mn> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">12.34</pre></td>
        <td valign="top"><pre lang="html">     

<math> <mrow> <mn>12.34</mn> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">12x</pre></td>
        <td valign="top"><pre lang="html">     

<math> <mrow> <mn>12</mn> <mi>x</mi> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">3-2</pre></td>
        <td valign="top"><pre lang="html">     

<math> <mrow> <mn>3</mn> <mo>−</mo> <mn>2</mn> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>

.. raw:: html

   </table>

Subscripts and Superscripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <table>

::

    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">a_b</pre></td>
        <td valign="top"><pre lang="html">

<math> <mrow> <msub> <mi>a</mi> <mi>b</mi> </msub> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">a^b</pre></td>
        <td valign="top"><pre lang="html">

<math> <mrow> <msup> <mi>a</mi> <mi>b</mi> </msup> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">a_b^c</pre></td>
        <td valign="top"><pre lang="html">

<math> <mrow> <msubsup> <mi>a</mi> <mi>b</mi> <mi>c</mi> </msubsup>
</mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>

.. raw:: html

   </table>

Fractions
~~~~~~~~~

.. raw:: html

   <table>

::

    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\frac{1}{2}</pre></td>
        <td valign="top"><pre lang="html">      

<math> <mrow> <mfrac> <mrow> <mn>1</mn> </mrow> <mrow> <mn>2</mn>
</mrow> </mfrac> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>

.. raw:: html

   </table>

Roots
~~~~~

.. raw:: html

   <table>

::

    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\sqrt{2}</pre></td>
        <td valign="top"><pre lang="html">      

<math> <mrow> <msqrt> <mrow> <mn>2</mn> </mrow> </msqrt> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\sqrt[3]{2}</pre></td>
        <td valign="top"><pre lang="html"> 

<math> <mrow> <mroot> <mrow> <mn>2</mn> </mrow> <mrow> <mn>3</mn>
</mrow> </mroot> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>

.. raw:: html

   </table>

Matrices
~~~~~~~~

.. raw:: html

   <table>

::

    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\begin{matrix}a & b \\ c & d \end{matrix}</pre></td>
        <td valign="top"><pre lang="html">

<math> <mrow> <mtable> <mtr> <mtd> <mi>a</mi> </mtd> <mtd> <mi>b</mi>
</mtd> </mtr> <mtr> <mtd> <mi>c</mi> </mtd> <mtd> <mi>d</mi> </mtd>
</mtr> </mtable> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\begin{matrix*}[r]a & b \\ c & d \end{matrix*}</pre></td>
        <td valign="top"><pre lang="html">

<math> <mrow> <mtable> <mtr> <mtd columnalign='right'> <mi>a</mi> </mtd>
<mtd columnalign='right'> <mi>b</mi> </mtd> </mtr> <mtr> <mtd
columnalign='right'> <mi>c</mi> </mtd> <mtd columnalign='right'>
<mi>d</mi> </mtd> </mtr> </mtable> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>
    <tr>
        <td valign="top"><pre lang="latex">

A\_{m,n} =

.. raw:: latex

   \begin{bmatrix}
     a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
     a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
     \vdots  & \vdots  & \ddots & \vdots  \\
     a_{m,1} & a_{m,2} & \cdots & a_{m,n} 
    \end{bmatrix}

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

        <td valign="top"><pre lang="html">

<math> <mrow> <msub> <mi>A</mi> <mrow> <mi>m</mi> <mi>,</mi> <mi>n</mi>
</mrow> </msub> <mo>=</mo> <mo>[</mo> <mtable> <mtr> <mtd> <msub>
<mi>a</mi> <mrow> <mn>1</mn> <mi>,</mi> <mn>1</mn> </mrow> </msub>
</mtd> <mtd> <msub> <mi>a</mi> <mrow> <mn>1</mn> <mi>,</mi> <mn>2</mn>
</mrow> </msub> </mtd> <mtd> <mo>⋯</mo> </mtd> <mtd> <msub> <mi>a</mi>
<mrow> <mn>1</mn> <mi>,</mi> <mi>n</mi> </mrow> </msub> </mtd> </mtr>
<mtr> <mtd> <msub> <mi>a</mi> <mrow> <mn>2</mn> <mi>,</mi> <mn>1</mn>
</mrow> </msub> </mtd> <mtd> <msub> <mi>a</mi> <mrow> <mn>2</mn>
<mi>,</mi> <mn>2</mn> </mrow> </msub> </mtd> <mtd> <mo>⋯</mo> </mtd>
<mtd> <msub> <mi>a</mi> <mrow> <mn>2</mn> <mi>,</mi> <mi>n</mi> </mrow>
</msub> </mtd> </mtr> <mtr> <mtd> <mo>⋮</mo> </mtd> <mtd> <mo>⋮</mo>
</mtd> <mtd> <mo>⋱</mo> </mtd> <mtd> <mo>⋮</mo> </mtd> </mtr> <mtr>
<mtd> <msub> <mi>a</mi> <mrow> <mi>m</mi> <mi>,</mi> <mn>1</mn> </mrow>
</msub> </mtd> <mtd> <msub> <mi>a</mi> <mrow> <mi>m</mi> <mi>,</mi>
<mn>2</mn> </mrow> </msub> </mtd> <mtd> <mo>⋯</mo> </mtd> <mtd> <msub>
<mi>a</mi> <mrow> <mi>m</mi> <mi>,</mi> <mi>n</mi> </mrow> </msub>
</mtd> </mtr> </mtable> <mo>]</mo> </mrow> </math>

.. raw:: html

   </pre>

.. raw:: html

   </td>

::

    </tr>

.. raw:: html

   </table>

References
~~~~~~~~~~

LaTeX
^^^^^

-  https://en.wikibooks.org/wiki/LaTeX/Mathematics
-  http://artofproblemsolving.com/wiki/index.php?title=Main\_Page
-  http://milde.users.sourceforge.net/LUCR/Math/
-  http://www.forkosh.com/mimetextutorial.html

MathML
^^^^^^

-  http://www.xmlmind.com/tutorials/MathML/

Author
~~~~~~

-  `Ronie Martinez <mailto:ronmarti18@gmail.com>`__

.. |version| image:: https://img.shields.io/pypi/v/latex2mathml.svg
.. |license| image:: https://img.shields.io/pypi/l/latex2mathml.svg
.. |status| image:: https://img.shields.io/pypi/status/latex2mathml.svg

