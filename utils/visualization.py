
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_sales_plot(df):
    os.makedirs('static/plots', exist_ok=True)

    
    if 'Month' not in df.columns or 'Sales' not in df.columns:
        raise KeyError("Required columns 'Month' and 'Sales' not found in the dataset")

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='Month', y='Sales', marker='o')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Sales')
    plot_path = 'static/plots/sales_plot.png'
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return plot_path

def generate_churn_pie_chart(predictions):
    os.makedirs('static/plots', exist_ok=True)

    churn_counts = predictions.value_counts()
    labels = churn_counts.index.astype(str)
    sizes = churn_counts.values

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['lightcoral', 'lightgreen'])
    plt.title('Customer Churn Distribution')
    plot_path = 'static/plots/churn_pie_chart.png'
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return plot_path
