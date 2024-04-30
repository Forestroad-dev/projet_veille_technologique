import { recommender } from '@/components/model/call_model'

export default async function handler(req, res) {
  const { search } = req.query;

  try {
    // Appeler la fonction de recommandation avec le terme de recherche
    const recommendedProducts = recommender(search);

    // Envoyer les produits recommandés dans la réponse
    res.status(200).json({ products: recommendedProducts });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Une erreur s'est produite lors de la récupération des recommandations." });
  }
}
