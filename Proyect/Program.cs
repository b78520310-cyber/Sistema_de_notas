string nombre;
string apellido;
int edad;
double altura;

Console.Write("Ingrese su nombre: ");
nombre = Console.ReadLine();

Console.Write("Ingrese su apellido: ");
apellido = Console.ReadLine();

Console.Write("Ingrese su edad: ");
edad = Convert.ToInt32(Console.ReadLine());

Console.Write("Ingrese su altura: ");

while (!double.TryParse(Console.ReadLine(), out altura))
{
    Console.Write("Valor inválido. Ingrese la altura nuevamente: ");
}

Console.WriteLine("\n--- Datos ingresados ---");
Console.WriteLine($"Nombre: {nombre}");
Console.WriteLine($"Apellido: {apellido}");
Console.WriteLine($"Edad: {edad}");
Console.WriteLine($"Altura: {altura} metros");

Console.WriteLine($"\nHola, mi nombre es {nombre} {apellido}, tengo {edad} años y mido {altura} metros.");
