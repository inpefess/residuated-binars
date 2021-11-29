FROM inpefess/isabelle-client:latest
COPY examples/example.ipynb $HOME/residuated-binars-example.ipynb
COPY residuated_binars $HOME/residuated_binars
ENV PATH $HOME/.local/bin:${PATH}
ENV PYTHONPATH $HOME/residuated_binars:${PYTHONPATH}
