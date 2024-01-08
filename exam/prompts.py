baseline_prompt = """
{question}

Answer the question, then start a new line and say "Final Answer:" and indicate the letter choice of your final answer. If you think none of the options are correct, then write "Final Answer: abstain" instead.
"""

# Problems and Explanations all taken from 2021 Fall AMC Exams
# Problem 1 on AMC 10A and 12A
# Problem 4 on 2021 AMC 10A and 3 on 12A
cot_easy = r"""
Question: What is the value of $\frac{(2112-2021)^2}{169}$? $A) 7 B) 21 C) 49 D) 64 E) 91$
Answer: We have\[\frac{(2112-2021)^2}{169}=\frac{91^2}{169}=\frac{91^2}{13^2}=\left(\frac{91}{13}\right)^2=7^2=\boxed{\textbf{(C) } 49}.\]
Final Answer: C.

Question: Menkara has a $4 \times 6$ index card. If she shortens the length of one side of this card by $1$ inch, the card would have area $18$ square inches. What would the area of the card be in square inches if instead she shortens the length of the other side by $1$ inch? $A) 16 B) 17 C) 18 D) 19 E) 20$
Answer: If Mr. Lopez chooses Route A, then he will spend $\frac{6}{30}=\frac{1}{5}$ hour, or $\frac{1}{5}\cdot60=12$ minutes.
If Mr. Lopez chooses Route B, then he will spend $\frac{9/2}{40}+\frac{1/2}{20}=\frac{11}{80}$ hour, or $\frac{11}{80}\cdot60=8\frac14$ minutes.
Therefore, Route B is quicker than Route A by $12-8\frac14=\boxed{\textbf{(B)}\  3 \frac{3}{4}}$ minutes.
Final Answer: B.
"""

# Problem 10 on AMC 10A and 7 on 12A
# Problem 12 on AMC 10A and 10 on 12A
cot_mid = r"""
Question: A school has $100$ students and $5$ teachers. In the first period, each student is taking one class, and each teacher is teaching one class. The enrollments in the classes are $50, 20, 20, 5,$ and $5$. Let $t$ be the average value obtained if a teacher is picked at random and the number of students in their class is noted. Let $s$ be the average value obtained if a student was picked at random and the number of students in their class, including the student, is noted. What is $t-s$? $A) -18.5  B) -13.5 C) 0 D) 13.5 E) 18.5$
Answer: The formula for expected values is\[\text{Expected Value}=\sum(\text{Outcome}\cdot\text{Probability}).\]We have\begin{align*} t &= 50\cdot\frac15 + 20\cdot\frac15 + 20\cdot\frac15 + 5\cdot\frac15 + 5\cdot\frac15 \\ &= (50+20+20+5+5)\cdot\frac15 \\ &= 100\cdot\frac15 \\ &= 20, \\ s &= 50\cdot\frac{50}{100} + 20\cdot\frac{20}{100} + 20\cdot\frac{20}{100} + 5\cdot\frac{5}{100} + 5\cdot\frac{5}{100} \\ &= 25 + 4 + 4 + 0.25 + 0.25 \\ &= 33.5. \end{align*}Therefore, the answer is $t-s=\boxed{\textbf{(B)}\ {-}13.5}.$
Final Answer: B.

Question: The base-nine representation of the number $N$ is $27{,}006{,}000{,}052_{\text{nine}}.$ What is the remainder when $N$ is divided by $5?$ $A) 0B) 1C) 2D) 3E)4$
Answer: Recall that $9\equiv-1\pmod{5}.$ We expand $N$ by the definition of bases:\begin{align*} N&=27{,}006{,}000{,}052_9 \\ &= 2\cdot9^{10} + 7\cdot9^9 + 6\cdot9^6 + 5\cdot9 + 2 \\ &\equiv 2\cdot(-1)^{10} + 7\cdot(-1)^9 + 6\cdot(-1)^6 + 5\cdot(-1) + 2 &&\pmod{5} \\ &\equiv 2-7+6-5+2 &&\pmod{5} \\ &\equiv -2 &&\pmod{5} \\ &\equiv \boxed{\textbf{(D) } 3} &&\pmod{5}. \end{align*}
Final Answer: D.
"""

# Problem 23 on AMC 10A and 20 on 12A
# Problem 25 on AMC 10A and 23 on 12A
cot_hard = r"""
Question: For each positive integer $n$, let $f_1(n)$ be twice the number of positive integer divisors of $n$, and for $j \ge 2$, let $f_j(n) = f_1(f_{j-1}(n))$. For how many values of $n \le 50$ is $f_{50}(n) = 12?$ $A)7 B)8 C)9 D)10 E)11$
Answer: First, we can test values that would make $f(x)=12$ true. For this to happen $x$ must have $6$ divisors, which means its prime factorization is in the form $pq^2$ or $p^5$, where $p$ and $q$ are prime numbers. Listing out values less than $50$ which have these prime factorizations, we find $12,18,20,28,44,45,50$ for $pq^2$, and just $32$ for $p^5$. Here $12$ especially catches our eyes, as this means if one of $f_i(n)=12$, each of $f_{i+1}(n), f_{i+2}(n), ...$ will all be $12$. This is because $f_{i+1}(n)=f(f_i(n))$ (as given in the problem statement), so were $f_i(n)=12$, plugging this in we get $f_{i+1}(n)=f(12)=12$, and thus the pattern repeats. Hence, as long as for a $i$, such that $i\leq 50$ and $f_{i}(n)=12$, $f_{50}(n)=12$ must be true, which also immediately makes all our previously listed numbers, where $f(x)=12$, possible values of $n$.
We also know that if $f(x)$ were to be any of these numbers, $x$ would satisfy $f_{50}(n)$ as well. Looking through each of the possibilities aside from $12$, we see that $f(x)$ could only possibly be equal to $20$ and $18$, and still have $x$ less than or equal to $50$. This would mean $x$ must have $10$, or $9$ divisors, and testing out, we see that $x$ will then be of the form $p^4q$, or $p^2q^2$. The only two values less than or equal to $50$ would be $48$ and $36$ respectively. From here there are no more possible values, so tallying our possibilities we count $\boxed{\textbf{(D) }10}$ values (Namely $12,18,20,28,32,36,44,45,48,50$).
Final Answer: D. 

Question: A quadratic polynomial with real coefficients and leading coefficient $1$ is called $\emph{disrespectful}$ if the equation $p(p(x))=0$ is satisfied by exactly three real numbers. Among all the disrespectful quadratic polynomials, there is a unique such polynomial $\tilde{p}(x)$ for which the sum of the roots is maximized. What is $\tilde{p}(1)$? $A) \dfrac{5}{16} B) \dfrac{1}{2} C) \dfrac{5}{8} D) 1 E) \dfrac{9}{8}$
Answer: Let $r_1$ and $r_2$ be the roots of $\tilde{p}(x)$. Then, $\tilde{p}(x)=(x-r_1)(x-r_2)=x^2-(r_1+r_2)x+r_1r_2$. The solutions to $\tilde{p}(\tilde{p}(x))=0$ is the union of the solutions to\[\tilde{p}(x)-r_1=x^2-(r_1+r_2)x+(r_1r_2-r_1)=0\]and\[\tilde{p}(x)-r_2=x^2-(r_1+r_2)x+(r_1r_2-r_2)=0.\]Note that one of these two quadratics has one solution (a double root) and the other has two as there are exactly three solutions. WLOG, assume that the quadratic with one root is $x^2-(r_1+r_2)x+(r_1r_2-r_1)=0$. Then, the discriminant is $0$, so $(r_1+r_2)^2 = 4r_1r_2 - 4r_1$. Thus, $r_1-r_2=\pm 2\sqrt{-r_1}$, but for $x^2-(r_1+r_2)x+(r_1r_2-r_2)=0$ to have two solutions, it must be the case that $r_1-r_2=- 2\sqrt{-r_1} (*)$. It follows that the sum of the roots of $\tilde{p}(x)$ is $2r_1 + 2\sqrt{-r_1}$, whose maximum value occurs when $r_1 = - \frac{1}{4} (\star)$. Solving for $r_2$ yields $r_2 = \frac{3}{4}$. Therefore, $\tilde{p}(x)=x^2 - \frac{1}{2} x - \frac{3}{16}$, so $\tilde{p}(1)= \boxed{A) \frac{5}{16}}$.
Remarks: For $x^2-(r_1+r_2)x+(r_1r_2-r_2)=0$ to have two solutions, the discriminant $(r_1+r_2)^2-4r_1r_2+4r_2$ must be positive. From here, we get that $(r_1-r_2)^2>-4r_2$, so $-4r_1>-4r_2 \implies r_1<r_2$. Hence, $r_1-r_2$ is negative, so $r_1-r_2=-2\sqrt{-r_1}$.
Set $\sqrt{-r_1}=x$. Now $r_1+\sqrt{-r_1}=-x^2+x$, for which the maximum occurs when $x=\frac{1}{2} \rightarrow r_1=-\frac{1}{4}$.
Final Answer: A.
"""

cot_prompt = f"""
{cot_easy}

{cot_mid}

{cot_hard}

""" + baseline_prompt 

prompts = {"baseline": baseline_prompt, "cot": cot_prompt}
