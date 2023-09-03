# Introdução à Inversão de Dados Geofísicos

Disciplina ministrada ao Programa de Pós-Graduação em Geociências da Faculdade de Geologia da Universidade do Estado do Rio de Janeiro (FGEL/UERJ).

**Professor**: [André Luis A. Reis](https://www.pinga-lab.org/people/andre.html)

**E-mails:** reisandreluis@gmail.com / andre.reis@uerj.br

>**Aviso:** O material disponibilizado neste repositório está em constante desenvolvimento e, portanto, a universidade e a coordenação de graduação não possuem qualquer responsabilidade sobre o seu conteúdo. As aulas não serão gravadas.

## Ementa

Revisão matemática: Matrizes e vetores. Espaços e subespaços vetoriais. Determinantes. Autovalores e autovetores. Sistemas de equações lineares. Séries de Taylor. Problema direto e problema inverso: Discretização e parametrização. Problemas lineares e não-lineares. Formulação matemática do problema inverso. Existência, unicidade e estabilidade das soluções. Regularização: como contornar
problemas mal-postos. Exemplos e aplicações na Geofísica.

Versão oficial do conteúdo da disciplina: [TEG: Introdução à inversão](https://www.fgel.uerj.br/site/wp-content/uploads/2021/05/Ementa_TEG_Introdu%c3%a7%c3%a3o-%c3%a0-invers%c3%a3o-de-dados-geof%c3%adsicos_Prof.-Andr%c3%a9-Luis-Reis.pdf)

## Tópicos do curso

* Noções básicas de Álgebra Linear e Cálculo vetorial
* O que é um problema inverso?
* Problema inverso linear e não-linear
* Existência, unicidade e estabilidade de soluções
* Tipos de regularização
* Aplicações na Geofísica

## Conteúdo didático computacional

>**Aviso:** Os códigos aqui apresentados são parte de uma disciplina e sua usabilidade é, consideravelmente, limitada a nível de pesquisa e desenvolvimento. A universidade não tem qualquer responsabilidade sobre a aplicação, tanto a nível acadêmico quanto profissional, dos códigos aqui apresentados.

- Introdução ao Python
  - [ ] Comandos básicos[[`pythonic_first_steps.ipynb`](https://github.com/andrelreis/introducao-inversao/blob/2023/1/Content/codes/First_steps_Python/1.%20pythonic_first_steps.ipynb)]
  - [ ] Noções de Álgebra Linear em Python

- Exemplos de problemas lineares
  - [x] Problemas de cinemática
    - [x] Movimento Uniforme[[`movimento_uniforme.ipynb`](Content/codes/Linear_inverse_problems/kinematic_problems/1.movimento_uniforme.ipynb)]
    - [x] Movimento Uniformemente Variado[[`movimento_uniforme_acelerado.ipynb`](Content/codes/Linear_inverse_problems/kinematic_problems/2.movimento_uniforme_acelerado.ipynb)]
  - [x] Estimativa da direção de corpos esféricos[[`magdir_sphere_estimation.ipynb`](Content/codes/Linear_inverse_problems/magnetization_direction_sphere/1.magdir_esfera_estimation.ipynb)]
  - [x] Camada equivalente
    - [x] Camada magnética com Norma mínima[[`magnetic_equivalent_layer_Tik0.ipynb`](Content/codes/Linear_inverse_problems/equivalent_layer/1.magnetic_equivalent_layer_Tik0.ipynb)]
    - [x] Camada magnética com Suavidade[[`magnetic_equivalent_layer_Tik1.ipynb`](Content/codes/Linear_inverse_problems/equivalent_layer/2.magnetic_equivalent_layer_Tik1.ipynb)]

- Exemplos de problemas não-lineares
  - Métodos determinísticos
    - [x] Função Rosenbrock
      - [x] Steepest descent [[`SD_rosenbrock.ipynb`](Content/codes/Non_linear_problems/Deterministic_methods/Rosenbrock_function/SD_rosenbrock.ipynb)]
      - [x] Método de Newton[[`Newton_rosenbrock.ipynb`](Content/codes/Non_linear_problems/Deterministic_methods/Rosenbrock_function/Newton_rosenbrock.ipynb)]
      - [x] Método de Gauss-Newton[[`GN_rosenbrock.ipynb`](Content/codes/Non_linear_problems/Deterministic_methods/Rosenbrock_function/GN_rosenbrock.ipynb)]
      - [x] Método de Levenberg-Marquardt[[`LM_rosenbrock.ipynb`](Content/codes/Non_linear_problems/Deterministic_methods/Rosenbrock_function/GN_rosenbrock.ipynb)]
    - [x] Determinação epicentral simples[[`simple_epicenter_determination.ipynb`](Content/codes/Non_linear_problems/Deterministic_methods/Epicentral_determination/simple_epicenter_estimation.ipynb)]
    - [x] Estimativa 2D do relevo de um embasamento[[`2D_basement_estimation.ipynb`](Content/codes/Non_linear_problems/Deterministic_methods/Basement_estimation/1.2D_basement_estimation.ipynb)]
  - Métodos Heurísticos
    - [x] Função Rastrigin
      - [x] Simulated Annealing[[`SA_rastrigin_function.ipynb`](Content/codes/Non_linear_problems/Heuristic_method/SA_rastrigin_function.ipynb)]
      - [x] Genetic Algorithm[[`AG_rastrigin_function.ipynb`](Content/codes/Non_linear_problems/Heuristic_method/AG_rastrigin_function.ipynb)]

## Referências bibliográficas

* Aster, R. C., Borchers, B., and Thurber, C. H. 2005. *Parameter Estimation and Inverse Problems* , Academic Press Inc.

* Bard, Y. 1974. *Nonlinear parameter estimation*. Academic Press Inc.

* Kelley, C. T. 1999. *Iterative methods for optimization: Raleigh*. SIAM.
* Menke, W. 1989. *Geophysical data analysis: Discrete inverse theory*. Academic Press Inc.

* Parker, R. L. 1977. *Understanding inverse theory*. Ann. Rev.Earth. Planet. Sci., v. 5, p. 35-64.

* Tikhonov., A. N. e Arsenin, V. Y. 1977. *Solutions of ill-posed problems*. John Wiley and Sons.

* Periódicos da área

## Material

Todo o material da disciplina (dados e códigos computacionais) estão disponíveis em um repositório no Github:

https://github.com/andrelreis/introducao-inversao

As versões ao final de cada ano são marcadas com um *tag* e podem ser vistas em:

https://github.com/andrelreis/introducao-inversao/releases


## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">"Material didático da disciplina Introdução à inversão"</span>
by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/andrelreis/metodos-potenciais" property="cc:attributionName" rel="cc:attributionURL">André L A Reis</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
