FROM inpefess/isabelle-client:latest
USER root
RUN apt-get update && apt-get -y install python3-graphviz
COPY examples/*.ipynb /home/isabelle/
COPY residuated_binars /home/isabelle/residuated_binars
RUN chown -R isabelle:isabelle /home/isabelle/*.ipynb
USER isabelle
ENV PATH $HOME/.local/bin:${PATH}
ENV PYTHONPATH $HOME/residuated_binars:${PYTHONPATH}
