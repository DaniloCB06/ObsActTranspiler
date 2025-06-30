#include <stdio.h>

// protótipos das funções ObsAct → C
void ligar(const char* dev);
void desligar(const char* dev);
void alerta(const char* dev, const char* msg);
void alerta_var(const char* dev, const char* msg, int var);

int main() {
    int Temp = 0;
    int Umidade = 0;

    Temp = 30;
    Umidade = 85;
    Temp = Umidade;
    if ((Temp > 28) && (Umidade > 80)) { alerta("Display", "Calor e umidade alta!"); }
    if ((Temp > 28) && (Umidade > 80)) { ligar("Ventoinha"); } else { desligar("Ventoinha"); }
    if (Temp > 35) { alerta_var("Display", "Aviso: temperatura ", Temp); alerta_var("Ventoinha", "Aviso: temperatura ", Temp); }

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