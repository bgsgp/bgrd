using bgrd.ViewModels;
using System.Windows;

namespace bgrd;

public partial class MainWindow : Window
{
    public MainWindow(MainViewModel viewModel)
    {
        InitializeComponent();
        DataContext = viewModel;
    }
}
