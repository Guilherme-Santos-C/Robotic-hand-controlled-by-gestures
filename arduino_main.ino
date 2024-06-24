#include <Servo.h>

Servo motor_indicador;
Servo motor_meio;
Servo motor_anelar;
Servo motor_mindinho;
Servo motor_polegar;

void acionar_motor(Servo motor, char intensidade) {
  if (intensidade == '0') {
    motor.write(0);
  }
  else if (intensidade == '1') {
    motor.write(60);
  }
  else if (intensidade == '2') {
    motor.write(120);
  }
  else if (intensidade == '3') {
    motor.write(180);
  }
}

void setup() {
  motor_indicador.attach(3);
  motor_meio.attach(5);
  motor_anelar.attach(6);
  motor_mindinho.attach(9);
  motor_polegar.attach(10);
  motor_indicador.write(0);
  motor_meio.write(0);
  motor_anelar.write(0);
  motor_mindinho.write(0);
  motor_polegar.write(0);
  Serial.begin(9600);
  // Aguarda até que a porta serial esteja pronta
  while (!Serial) {
    ; 
  }
}

void loop() {
  if (Serial.available() > 0) {
    String forca_motores = Serial.readStringUntil('\n');
    if (forca_motores.length() >= 2) { 
      acionar_motor(motor_indicador, forca_motores[0]);
      acionar_motor(motor_meio, forca_motores[1]);
      acionar_motor(motor_anelar, forca_motores[2]);
      acionar_motor(motor_mindinho, forca_motores[3]);
      acionar_motor(motor_polegar, forca_motores[4]);
    }
  }
}
