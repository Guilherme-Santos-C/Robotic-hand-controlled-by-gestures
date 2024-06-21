#include <Servo.h>

Servo motor_indicador;
Servo motor_meio;
Servo motor_anelar;
Servo motor_mindinho;
Servo motor_polegar;

void acionar_motor(Servo motor, char intensidade) {
  if(intensidade == '0') {
    motor.write(60);
  }
  else if(intensidade == '1') {
    motor.write(180); 
  }
  else if(intensidade == '2') {
    motor.write(180);
  }
  else if(intensidade == '3') {
    motor.write(0);
  }
}

void setup() {
  motor_indicador.attach(3);
  motor_meio.attach(5);
  motor_anelar.attach(6);
  motor_mindinho.attach(9);
  motor_polegar.attach(10);
  Serial.begin(9600);
  // Aguarda até que a porta serial esteja pronta
 while (!Serial) {
   ; // Espera até que a porta serial esteja conectada
 }
}

void loop() {
  if (Serial.available() > 0) {
    String forca_motores = Serial.readStringUntil('\n');
    acionar_motor(motor_indicador, forca_motores[0]);
    acionar_motor(motor_meio, forca_motores[1]);
    acionar_motor(motor_anelar, forca_motores[2]);
    acionar_motor(motor_mindinho, forca_motores[3]);
    acionar_motor(motor_polegar, forca_motores[4]);
  }
}
