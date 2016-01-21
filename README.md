![version](https://img.shields.io/pypi/v/latex2mathml.svg)![license](https://img.shields.io/pypi/l/latex2mathml.svg)![status](https://img.shields.io/pypi/status/latex2mathml.svg)

# latex2mathml
Pure Python library for LaTeX to MathML conversion.

## Demo
[latex2mathml Demo](http://www.roniemartinez.space/latex2mathml)

## Usage

```python
import latex2mathml

latex_input = "<your_latex_string>"
mathml_output = latex2mathml.convert(latex_input)
```

## Examples

### Identifiers, Numbers and Operators

#### LaTeX Input
```latex
x
```

#### MathML Output
```html
<math>
    <mrow>
        <mi>x</mi>
    </mrow>
</math>
```

#### LaTeX Input
```latex
xyz
```

#### MathML Output
```html
<math>
    <mrow>
        <mi>x</mi>
        <mi>y</mi>
        <mi>z</mi>
    </mrow>
</math>
```

#### LaTeX Input
```latex
3
```

#### MathML Output
```html
<math>
    <mrow>
        <mn>3</mn>
    </mrow>
</math>
```

#### LaTeX Input
```latex
444
```

#### MathML Output
```html
<math>
    <mrow>
        <mn>444</mn>
    </mrow>
</math>
```

#### LaTeX Input
```latex
12.34
```

#### MathML Output
```html
<math>
    <mrow>
        <mn>12.34</mn>
    </mrow>
</math>
```

#### LaTeX Input
```latex
12x
```

#### MathML Output
```html
<math>
    <mrow>
        <mn>12</mn>
        <mi>x</mi>
    </mrow>
</math>
```

#### LaTeX Input
```latex
3-2
```

#### MathML Output
```html
<math>
    <mrow>
        <mn>3</mn>
        <mo>&#x02212;</mo>
        <mn>2</mn>
    </mrow>
</math>
```

### Subscripts and Superscripts

#### LaTeX Input
```latex
a_b
```

#### MathML Output
```html
<math>
    <mrow>
        <msub>
            <mi>a</mi>
            <mi>b</mi>
        </msub>
    </mrow>
</math>
```

#### LaTeX Input
```latex
a^b
```

#### MathML Output
```html
<math>
    <mrow>
        <msup>
            <mi>a</mi>
            <mi>b</mi>
        </msup>
    </mrow>
</math>
```

#### LaTeX Input
```latex
a_b^c
```

#### MathML Output
```html
<math>
    <mrow>
        <msubsup>
            <mi>a</mi>
            <mi>b</mi>
            <mi>c</mi>
        </msubsup>
    </mrow>
</math>
```

### Fractions

#### LaTeX Input
```latex
\frac{1}{2}
```

#### MathML Output
```html
<math>
    <mrow>
        <mfrac>
            <mrow>
                <mn>1</mn>
            </mrow>
            <mrow>
                <mn>2</mn>
            </mrow>
        </mfrac>
    </mrow>
</math>
```

### Roots

#### LaTeX Input
```latex
\sqrt{2}
```

#### MathML Output
```html
<math>
    <mrow>
        <msqrt>
            <mrow>
                <mn>2</mn>
            </mrow>
        </msqrt>
    </mrow>
</math>
```

#### LaTeX Input
```latex
\sqrt[3]{2}
```

#### MathML Output
```html
<math>
    <mrow>
        <mroot>
            <mrow>
                <mn>2</mn>
            </mrow>
            <mrow>
                <mn>3</mn>
            </mrow>
        </mroot>
    </mrow>
</math>
```

### Matrices

#### LaTeX Input
```latex
\begin{matrix}a & b \\ c & d \end{matrix}
```

#### MathML Output
```html
<math>
    <mrow>
        <mtable>
            <mtr>
                <mtd>
                    <mi>a</mi>
                </mtd>
                <mtd>
                    <mi>b</mi>
                </mtd>
            </mtr>
            <mtr>
                <mtd>
                    <mi>c</mi>
                </mtd>
                <mtd>
                    <mi>d</mi>
                </mtd>
            </mtr>
        </mtable>
    </mrow>
</math>
```

#### LaTeX Input
```latex
\begin{matrix*}[r]a & b \\ c & d \end{matrix*}
```

#### MathML Output
```html
<math>
    <mrow>
        <mtable>
            <mtr>
                <mtd columnalign='right'>
                    <mi>a</mi>
                </mtd>
                <mtd columnalign='right'>
                    <mi>b</mi>
                </mtd>
            </mtr>
            <mtr>
                <mtd columnalign='right'>
                    <mi>c</mi>
                </mtd>
                <mtd columnalign='right'>
                    <mi>d</mi>
                </mtd>
            </mtr>
        </mtable>
    </mrow>
</math>
```

#### LaTeX Input
```latex
A_{m,n} = 
 \begin{bmatrix}
  a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
  a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
  \vdots  & \vdots  & \ddots & \vdots  \\
  a_{m,1} & a_{m,2} & \cdots & a_{m,n} 
 \end{bmatrix}
```

#### MathML Output
```html
<math>
    <mrow>
        <msub>
            <mi>A</mi>
            <mrow>
                <mi>m</mi>
                <mi>,</mi>
                <mi>n</mi>
            </mrow>
        </msub>
        <mo>&#x0003D;</mo>
        <mo>&#x0005B;</mo>
        <mtable>
            <mtr>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mn>1</mn>
                            <mi>,</mi>
                            <mn>1</mn>
                        </mrow>
                    </msub>
                </mtd>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mn>1</mn>
                            <mi>,</mi>
                            <mn>2</mn>
                        </mrow>
                    </msub>
                </mtd>
                <mtd>
                    <mo>&#x022EF;</mo>
                </mtd>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mn>1</mn>
                            <mi>,</mi>
                            <mi>n</mi>
                        </mrow>
                    </msub>
                </mtd>
            </mtr>
            <mtr>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mn>2</mn>
                            <mi>,</mi>
                            <mn>1</mn>
                        </mrow>
                    </msub>
                </mtd>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mn>2</mn>
                            <mi>,</mi>
                            <mn>2</mn>
                        </mrow>
                    </msub>
                </mtd>
                <mtd>
                    <mo>&#x022EF;</mo>
                </mtd>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mn>2</mn>
                            <mi>,</mi>
                            <mi>n</mi>
                        </mrow>
                    </msub>
                </mtd>
            </mtr>
            <mtr>
                <mtd>
                    <mo>&#x022EE;</mo>
                </mtd>
                <mtd>
                    <mo>&#x022EE;</mo>
                </mtd>
                <mtd>
                    <mo>&#x022F1;</mo>
                </mtd>
                <mtd>
                    <mo>&#x022EE;</mo>
                </mtd>
            </mtr>
            <mtr>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mi>m</mi>
                            <mi>,</mi>
                            <mn>1</mn>
                        </mrow>
                    </msub>
                </mtd>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mi>m</mi>
                            <mi>,</mi>
                            <mn>2</mn>
                        </mrow>
                    </msub>
                </mtd>
                <mtd>
                    <mo>&#x022EF;</mo>
                </mtd>
                <mtd>
                    <msub>
                        <mi>a</mi>
                        <mrow>
                            <mi>m</mi>
                            <mi>,</mi>
                            <mi>n</mi>
                        </mrow>
                    </msub>
                </mtd>
            </mtr>
        </mtable>
        <mo>&#x0005D;</mo>
    </mrow>
</math>
```

### References
#### LaTeX
* https://en.wikibooks.org/wiki/LaTeX/Mathematics
* http://artofproblemsolving.com/wiki/index.php?title=Main_Page
* http://milde.users.sourceforge.net/LUCR/Math/
* http://www.forkosh.com/mimetextutorial.html

#### MathML
* http://www.xmlmind.com/tutorials/MathML/
* https://github.com/fred-wang/mathml.css


### Author
* Ronie Martinez (ronmarti18@gmail.com)
