FROM inpefess/isabelle-client:latest
USER root
RUN apt-get update && apt-get -y install python3-graphviz
COPY examples/reproducing-papers.ipynb \
    /home/isabelle/reproduce-residuated-binars-papers.ipynb
COPY examples/lattice-example.ipynb /home/isabelle/lattice-example.ipynb
COPY residuated_binars /home/isabelle/residuated_binars
RUN chown -R isabelle:isabelle /home/isabelle/*.ipynb
USER isabelle
ENV PATH $HOME/.local/bin:${PATH}
ENV PYTHONPATH $HOME/residuated_binars:${PYTHONPATH}
