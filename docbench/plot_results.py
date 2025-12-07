import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('collections-export-2025-12-07.csv')

model_scores = df.groupby('model')['total_score'].mean()

df_plot = pd.DataFrame({
    'model': model_scores.index,
    'score': model_scores.values
})
df_plot['organization'] = df_plot['model'].str.split('/').str[0]
df_plot['model_name'] = df_plot['model'].str.split('/').str[1]

df_plot = df_plot.sort_values(['organization', 'score'], ascending=[True, False])

organization_colors = {
    'anthropic': '#CC785C',
    'openai': '#10A37F',
    'google': '#4285F4'
}

colors = [organization_colors.get(org, '#888888') for org in df_plot['organization']]

plt.figure(figsize=(14, 7))
bars = plt.bar(range(len(df_plot)), df_plot['score'].values, color=colors)

max_score = df_plot['score'].max()
margin = max_score * 0.1
plt.ylim(1500, max_score + margin)

plt.xticks(range(len(df_plot)), df_plot['model_name'], rotation=45, ha='right')
plt.xlabel('Model')
plt.ylabel('Average Score')
plt.title('Model Performance Comparison by Organization')
plt.tight_layout()

for i, score in enumerate(df_plot['score']):
    plt.text(i, score + max_score * 0.01, f'{score:.1f}',
             ha='center', va='bottom', fontsize=9)

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=org.capitalize())
                   for org, color in organization_colors.items()
                   if org in df_plot['organization'].values]
plt.legend(handles=legend_elements, loc='best')

plt.savefig('model_scores.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nAverage scores by model:")
print(df_plot[['model', 'score']].to_string(index=False))
