#include <stdio.h>

// protótipos das funções ObsAct → C
void ligar(const char* dev);
void desligar(const char* dev);
void alerta(const char* dev, const char* msg);
void alerta_var(const char* dev, const char* msg, int var);

int main() {
    int abertura = 0;
    int alarme = 0;

    abertura = 0;
    alarme = 0;
    if (abertura == 1) { alerta("janela", "Janela aberta!"); }
    if (alarme >= 1) { ligar("sirene"); } else { desligar("sirene"); }
    alerta_var("termostato", "Status geral", alarme);
    alerta_var("janela", "Status geral", alarme);
    alerta_var("sirene", "Status geral", alarme);

    return 0;
}

// implementações das funções
void ligar(const char* dev) { printf("%s ligado !\n", dev); }
void desligar(const char* dev) { printf("%s desligado !\n", dev); }
void alerta(const char* dev, const char* msg) {
    printf("%s recebeu o alerta :\n", dev);
    printf("%s\n", msg);
}
void alerta_var(const char* dev, const char* msg, int var) {
    printf("%s recebeu o alerta :\n", dev);
    printf("%s %d\n", msg, var);
}