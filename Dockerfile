FROM inpefess/isabelle-client:latest
USER root
RUN apt-get update && apt-get -y install python3-graphviz
USER isabelle
COPY examples/example.ipynb $HOME/residuated-binars-example.ipynb
COPY examples/lattice-example.ipynb $HOME/lattice-example.ipynb
COPY residuated_binars $HOME/residuated_binars
ENV PATH $HOME/.local/bin:${PATH}
ENV PYTHONPATH $HOME/residuated_binars:${PYTHONPATH}
