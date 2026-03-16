public class AreaRectangulo {

    // 1. Declaración del método
    public static double calcularArea(double base, double altura) {

        // 3. Realizar el cálculo
        double area = base * altura;

        // 4. Retornar el resultado
        return area;
    }

    public static void main(String[] args) {

        // Valores de ejemplo
        double base = 5;
        double altura = 3;

        // 5. Llamar al método
        double resultado = calcularArea(base, altura);

        // Mostrar resultado en consola
        System.out.println("El área del rectángulo es: " + resultado);
    }
}