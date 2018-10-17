# latex2mathml

Pure Python library for LaTeX to MathML conversion

<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/latex2mathml.svg'></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/latex2mathml.svg'></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://travis-ci.org/Code-ReaQtor/latex2mathml.svg?branch=master'></td>
        <td>Coverage</td>
        <td><img src='https://codecov.io/gh/Code-ReaQtor/latex2mathml/branch/master/graph/badge.svg'></td>
    </tr>
    <tr>
        <td>AppVeyor</td>
        <td><img src='https://ci.appveyor.com/api/projects/status/9f4qhc3ko880dr59/branch/master?svg=true'></td>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/latex2mathml.svg'></td>
    </tr>
    <tr>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/latex2mathml.svg'></td>
        <td>Implementation</td>
        <td><img src='https://img.shields.io/pypi/implementation/latex2mathml.svg'></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><img src='https://img.shields.io/pypi/status/latex2mathml.svg'></td>
        <td>Show your support</td>
        <td><a href='https://saythanks.io/to/Code-ReaQtor'><img src='https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg'></a></td>
    </tr>
</table>

## Installation

```bash
pip install latex2mathml
```

## Usage

```python
import latex2mathml.converter

latex_input = "<your_latex_string>"
mathml_output = latex2mathml.converter.convert(latex_input)
```

## Examples

### Identifiers, Numbers and Operators

<table>
    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">x</pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mi&gt;x&lt;/mi&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">xyz</pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mi&gt;x&lt;/mi&gt;
        &lt;mi&gt;y&lt;/mi&gt;
        &lt;mi&gt;z&lt;/mi&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">3</pre></td>
        <td valign="top"><pre lang="html">     
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mn&gt;3&lt;/mn&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">444</pre></td>
        <td valign="top"><pre lang="html">     
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mn&gt;444&lt;/mn&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">12.34</pre></td>
        <td valign="top"><pre lang="html">     
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mn&gt;12.34&lt;/mn&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">12x</pre></td>
        <td valign="top"><pre lang="html">     
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mn&gt;12&lt;/mn&gt;
        &lt;mi&gt;x&lt;/mi&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">3-2</pre></td>
        <td valign="top"><pre lang="html">     
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mn&gt;3&lt;/mn&gt;
        &lt;mo&gt;&#x02212;&lt;/mo&gt;
        &lt;mn&gt;2&lt;/mn&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
</table>

### Subscripts and Superscripts

<table>
    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">a_b</pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;msub&gt;
            &lt;mi&gt;a&lt;/mi&gt;
            &lt;mi&gt;b&lt;/mi&gt;
        &lt;/msub&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">a^b</pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;msup&gt;
            &lt;mi&gt;a&lt;/mi&gt;
            &lt;mi&gt;b&lt;/mi&gt;
        &lt;/msup&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">a_b^c</pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;msubsup&gt;
            &lt;mi&gt;a&lt;/mi&gt;
            &lt;mi&gt;b&lt;/mi&gt;
            &lt;mi&gt;c&lt;/mi&gt;
        &lt;/msubsup&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
</table>

### Fractions

<table>
    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\frac{1}{2}</pre></td>
        <td valign="top"><pre lang="html">      
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mfrac&gt;
            &lt;mrow&gt;
                &lt;mn&gt;1&lt;/mn&gt;
            &lt;/mrow&gt;
            &lt;mrow&gt;
                &lt;mn&gt;2&lt;/mn&gt;
            &lt;/mrow&gt;
        &lt;/mfrac&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
</table>

### Roots

<table>
    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\sqrt{2}</pre></td>
        <td valign="top"><pre lang="html">      
&lt;math&gt;
    &lt;mrow&gt;
        &lt;msqrt&gt;
            &lt;mrow&gt;
                &lt;mn&gt;2&lt;/mn&gt;
            &lt;/mrow&gt;
        &lt;/msqrt&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\sqrt[3]{2}</pre></td>
        <td valign="top"><pre lang="html"> 
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mroot&gt;
            &lt;mrow&gt;
                &lt;mn&gt;2&lt;/mn&gt;
            &lt;/mrow&gt;
            &lt;mrow&gt;
                &lt;mn&gt;3&lt;/mn&gt;
            &lt;/mrow&gt;
        &lt;/mroot&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
</table>

### Matrices

<table>
    <tr>
        <th>LaTeX Input</th>
        <th>MathML Output</th>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\begin{matrix}a & b \\ c & d \end{matrix}</pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mtable&gt;
            &lt;mtr&gt;
                &lt;mtd&gt;
                    &lt;mi&gt;a&lt;/mi&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mi&gt;b&lt;/mi&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
            &lt;mtr&gt;
                &lt;mtd&gt;
                    &lt;mi&gt;c&lt;/mi&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mi&gt;d&lt;/mi&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
        &lt;/mtable&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">\begin{matrix*}[r]a & b \\ c & d \end{matrix*}</pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;mtable&gt;
            &lt;mtr&gt;
                &lt;mtd columnalign='right'&gt;
                    &lt;mi&gt;a&lt;/mi&gt;
                &lt;/mtd&gt;
                &lt;mtd columnalign='right'&gt;
                    &lt;mi&gt;b&lt;/mi&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
            &lt;mtr&gt;
                &lt;mtd columnalign='right'&gt;
                    &lt;mi&gt;c&lt;/mi&gt;
                &lt;/mtd&gt;
                &lt;mtd columnalign='right'&gt;
                    &lt;mi&gt;d&lt;/mi&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
        &lt;/mtable&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
    <tr>
        <td valign="top"><pre lang="latex">
A_{m,n} = 
 \begin{bmatrix}
  a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
  a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
  \vdots  & \vdots  & \ddots & \vdots  \\
  a_{m,1} & a_{m,2} & \cdots & a_{m,n} 
 \end{bmatrix}
        </pre></td>
        <td valign="top"><pre lang="html">
&lt;math&gt;
    &lt;mrow&gt;
        &lt;msub&gt;
            &lt;mi&gt;A&lt;/mi&gt;
            &lt;mrow&gt;
                &lt;mi&gt;m&lt;/mi&gt;
                &lt;mi&gt;,&lt;/mi&gt;
                &lt;mi&gt;n&lt;/mi&gt;
            &lt;/mrow&gt;
        &lt;/msub&gt;
        &lt;mo&gt;&#x0003D;&lt;/mo&gt;
        &lt;mo&gt;&#x0005B;&lt;/mo&gt;
        &lt;mtable&gt;
            &lt;mtr&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mn&gt;1&lt;/mn&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mn&gt;1&lt;/mn&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mn&gt;1&lt;/mn&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mn&gt;2&lt;/mn&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mo&gt;&#x022EF;&lt;/mo&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mn&gt;1&lt;/mn&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mi&gt;n&lt;/mi&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
            &lt;mtr&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mn&gt;2&lt;/mn&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mn&gt;1&lt;/mn&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mn&gt;2&lt;/mn&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mn&gt;2&lt;/mn&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mo&gt;&#x022EF;&lt;/mo&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mn&gt;2&lt;/mn&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mi&gt;n&lt;/mi&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
            &lt;mtr&gt;
                &lt;mtd&gt;
                    &lt;mo&gt;&#x022EE;&lt;/mo&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mo&gt;&#x022EE;&lt;/mo&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mo&gt;&#x022F1;&lt;/mo&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mo&gt;&#x022EE;&lt;/mo&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
            &lt;mtr&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mi&gt;m&lt;/mi&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mn&gt;1&lt;/mn&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mi&gt;m&lt;/mi&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mn&gt;2&lt;/mn&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;mo&gt;&#x022EF;&lt;/mo&gt;
                &lt;/mtd&gt;
                &lt;mtd&gt;
                    &lt;msub&gt;
                        &lt;mi&gt;a&lt;/mi&gt;
                        &lt;mrow&gt;
                            &lt;mi&gt;m&lt;/mi&gt;
                            &lt;mi&gt;,&lt;/mi&gt;
                            &lt;mi&gt;n&lt;/mi&gt;
                        &lt;/mrow&gt;
                    &lt;/msub&gt;
                &lt;/mtd&gt;
            &lt;/mtr&gt;
        &lt;/mtable&gt;
        &lt;mo&gt;&#x0005D;&lt;/mo&gt;
    &lt;/mrow&gt;
&lt;/math&gt;
        </pre></td>
    </tr>
</table>

## References
### LaTeX

- https://en.wikibooks.org/wiki/LaTeX/Mathematics
- http://artofproblemsolving.com/wiki/index.php?title=Main_Page
- http://milde.users.sourceforge.net/LUCR/Math/
- http://www.forkosh.com/mimetextutorial.html

### MathML

- http://www.xmlmind.com/tutorials/MathML/

### Continuous Integration

- https://katyhuff.github.io/python-testing/08-ci/
- https://docs.travis-ci.com/user/caching/
- https://github.com/pypa/pip/blob/master/appveyor.yml


## Author
- [Ronie Martinez](mailto:ronmarti18@gmail.com)
